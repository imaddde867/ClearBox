from pydantic_settings import BaseSettings
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_cors_origins(cors_origins_env: str = None) -> List[str]:
    """Parse CORS origins from environment variable"""
    if cors_origins_env is None:
        cors_origins_env = os.getenv("CORS_ORIGINS", "*")
    return cors_origins_env.split(",")

class Settings(BaseSettings):
    """Base application settings"""
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./clearbox.db")
    
    # JWT Authentication
    secret_key: str = os.getenv("SECRET_KEY", "dev_secret_key_replace_in_production")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # MQTT
    mqtt_broker: str = os.getenv("MQTT_BROKER", "localhost")
    mqtt_port: int = int(os.getenv("MQTT_PORT", "1883"))
    mqtt_username: str = os.getenv("MQTT_USERNAME", "")
    mqtt_password: str = os.getenv("MQTT_PASSWORD", "")
    mqtt_use_ssl: bool = os.getenv("MQTT_USE_SSL", "false").lower() == "true"
    
    # Encryption
    encryption_key: str = os.getenv("ENCRYPTION_KEY", "dev_encryption_key_change_in_production")
    
    # CORS - Use the function to parse to List[str] properly
    cors_origins: List[str] = get_cors_origins()
    
    # General
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # For compatibility with pydantic-settings v2
    model_config = {
        "env_file": ".env",
    }
        
# Create a global settings object
try:
    settings = Settings()
except Exception as e:
    print(f"Error initializing settings: {e}")
    # Fallback settings with default values
    settings = Settings(
        database_url="sqlite:///./clearbox.db",
        cors_origins=["*"],
        debug=True
    ) 