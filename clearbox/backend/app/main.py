from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import logging
import importlib
import sys

from .database import engine, Base
from .models import User, Contact, ContactRequest, Message, Group, GroupMember
from .mqtt_client import setup_mqtt_client
from .config import settings

# Import routers
from .routes import auth, users, contacts, messages, notifications, websockets, groups

# Load environment variables
load_dotenv()

# Configure production settings if in production
if os.getenv("ENVIRONMENT", "development") == "production":
    try:
        # Try to import production settings
        from production import ProductionSettings
        production_settings = ProductionSettings()
        # Update the settings
        for key, value in production_settings.dict().items():
            if value is not None:  # Only update if the value is not None
                setattr(settings, key, value)
        logging.info("Using production settings")
    except ImportError:
        logging.warning("Production settings not found, using default settings")

# Set up logging
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="ClearBox API",
    description="Secure messaging API for ClearBox",
    version="1.0.0"
)

# Add CORS middleware with origins from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"CORS configured with origins: {settings.cors_origins}")

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
    return {
        "status": "API is running", 
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "db_type": "PostgreSQL" if "postgresql" in settings.database_url else "SQLite"
    }

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))

    # Run the FastAPI app
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)