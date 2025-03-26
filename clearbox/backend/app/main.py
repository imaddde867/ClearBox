from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import logging

from .database import engine, Base
from .models import User, Contact, ContactRequest, Message, Group, GroupMember
from .mqtt_client import setup_mqtt_client

# Import routers
from .routes import auth, users, contacts, messages, notifications, websockets, groups

# Load environment variables
load_dotenv()

# Get environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Create database tables
Base.metadata.create_all(bind=engine)

# Set up logging
logging_level = logging.DEBUG if ENVIRONMENT == "development" else logging.INFO
logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ClearBox API",
    description="Secure messaging API for ClearBox",
    version="1.0.0"
)

# Add HTTPS redirect middleware in production
if ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
    logger.info("HTTPS redirection enabled for production")

# Add CORS middleware with proper settings
if ENVIRONMENT == "development":
    # Development settings - allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS configured for development (allowing all origins)")
else:
    # Production settings - restrict to specific origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    logger.info(f"CORS configured for production with origins: {CORS_ORIGINS}")

# Security middleware for production
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    if ENVIRONMENT == "production":
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Set up MQTT client
try:
    setup_mqtt_client()
except Exception as e:
    logger.error(f"Failed to set up MQTT client: {e}")

# Include routers with prefixes
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(messages.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")
app.include_router(groups.router, prefix="/api")

# Include WebSocket router - WebSockets don't use /api prefix
app.include_router(websockets.router)

@app.get("/api")
def root():
    """
    Root endpoint to check if API is running
    """
    return {"status": "API is running", "version": "1.0.0"}

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))

    # Run the FastAPI app
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=ENVIRONMENT == "development")