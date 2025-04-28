import os
from app.config import Settings

class ProductionSettings(Settings):
    database_url: str = os.environ.get("DATABASE_URL")
    mqtt_broker: str = os.environ.get("MQTT_BROKER")
    mqtt_port: int = int(os.environ.get("MQTT_PORT", "8884"))
    mqtt_username: str = os.environ.get("MQTT_USERNAME")
    mqtt_password: str = os.environ.get("MQTT_PASSWORD")
    mqtt_use_ssl: bool = os.environ.get("MQTT_USE_SSL", "true").lower() == "true"
    secret_key: str = os.environ.get("SECRET_KEY")
    encryption_key: str = os.environ.get("ENCRYPTION_KEY")
    cors_origins: list = os.environ.get("CORS_ORIGINS", "https://clearbox.live").split(",")
    
    def dict(self):
        """
        Compatibility method for older code using dict() instead of model_dump()
        """
        return self.model_dump()