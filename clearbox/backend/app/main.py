from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import logging
import importlib
import sys
import traceback

from .database import engine, Base
from .models import User, Contact, ContactRequest, Message, Group, GroupMember
from .mqtt_client import setup_mqtt_client
from .config import settings

# Import routers
from .routes import auth, users, contacts, messages, notifications, websockets, groups

# Load environment variables
load_dotenv()

# Configure logging first for better debugging
logging_level = logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO
logging.basicConfig(level=logging_level, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Log environment information for debugging
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")

# Configure production settings if in production
if os.getenv("ENVIRONMENT", "development") == "production":
    try:
        # Try to import production settings using the absolute import path
        logger.info("Loading production settings...")
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logger.info(f"Backend directory: {backend_dir}")
        sys.path.append(backend_dir)
        
        try:
            from production import ProductionSettings
            production_settings = ProductionSettings()
            logger.info("Production settings class loaded successfully")
            
            # Update the settings - handle both Pydantic v1 and v2 versions
            try:
                # Pydantic v2 uses model_dump()
                settings_dict = production_settings.model_dump()
                logger.info("Used model_dump() for settings")
            except AttributeError:
                try:
                    # Pydantic v1 used dict()
                    settings_dict = production_settings.dict()
                    logger.info("Used dict() for settings")
                except AttributeError as e:
                    logger.error(f"Failed to convert settings to dict: {e}")
                    settings_dict = {}
            
            # Log the production settings for debugging (excluding sensitive info)
            safe_settings = {k: v for k, v in settings_dict.items() 
                             if k not in ['secret_key', 'encryption_key', 'mqtt_password', 'database_url']}
            logger.info(f"Production settings: {safe_settings}")
                    
            # Update settings with the values from production_settings
            for key, value in settings_dict.items():
                if value is not None:  # Only update if the value is not None
                    setattr(settings, key, value)
                    if key not in ['secret_key', 'encryption_key', 'mqtt_password', 'database_url']:
                        logger.info(f"Updated setting: {key} = {value}")
                    else:
                        logger.info(f"Updated setting: {key} = [REDACTED]")
                    
            logger.info("Production settings applied successfully")
        except ImportError as e:
            logger.error(f"Failed to import ProductionSettings: {e}")
            logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(f"Error loading production settings: {e}")
        logger.error(traceback.format_exc())

# Set up logging again with settings from config
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)

try:
    # Create database tables
    logger.info(f"Connecting to database: {settings.database_url.split('@')[1] if '@' in settings.database_url else 'SQLite'}")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    logger.error(traceback.format_exc())

# Initialize FastAPI app
app = FastAPI(
    title="ClearBox API",
    description="Secure messaging API for ClearBox",
    version="1.0.0"
)

# Log CORS settings
logger.info(f"Configuring CORS with origins: {settings.cors_origins}")

# Add CORS middleware with origins from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware configured successfully")

# Set up MQTT client
try:
    logger.info(f"Setting up MQTT client with broker: {settings.mqtt_broker}")
    setup_mqtt_client()
    logger.info("MQTT client set up successfully")
except Exception as e:
    logger.error(f"Failed to set up MQTT client: {e}")
    logger.error(traceback.format_exc())

# Include routers with prefixes
logger.info("Registering API routes...")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(messages.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")
app.include_router(groups.router, prefix="/api")

# Include WebSocket router - WebSockets don't use /api prefix
app.include_router(websockets.router)
logger.info("API routes registered successfully")

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

@app.get("/")
def index():
    """
    Root endpoint for the application
    """
    return {
        "message": "Welcome to ClearBox API",
        "documentation": "/docs",
        "api_status": "/api"
    }

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting FastAPI server on port {port}")

    # Run the FastAPI app
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)