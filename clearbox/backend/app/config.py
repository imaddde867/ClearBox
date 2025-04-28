from pydantic_settings import BaseSettings
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    
    # CORS - simplified to avoid parsing issues
    cors_origins_str: str = os.getenv("CORS_ORIGINS", "*")
    
    # General
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # For compatibility with pydantic-settings v2
    model_config = {
        "env_file": ".env",
    }
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from environment variable string"""
        if not self.cors_origins_str:
            return ["*"]
        return self.cors_origins_str.split(",")
        
# Create a global settings object
try:
    settings = Settings()
    print(f"Settings initialized: CORS origins = {settings.cors_origins}")
except Exception as e:
    print(f"Error initializing settings: {e}")
    # Fallback settings with default values
    settings = Settings(
        database_url="sqlite:///./clearbox.db",
        cors_origins_str="*",
        debug=True
    ) 