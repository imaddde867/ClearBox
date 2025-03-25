import paho.mqtt.client as mqtt
from paho.mqtt.publish import multiple
import json
import os
import logging
from dotenv import load_dotenv
#from .encryption import encrypt_message, decrypt_message

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = 60
MQTT_CLIENT_ID = "clearbox_server"

# Global client instance
mqtt_client = None

def on_connect(client, userdata, flags, rc):
    """Callback when client connects to the MQTT broker."""
    if rc == 0:
        logger.info(f"Connected to MQTT Broker: {MQTT_BROKER}")
    else:
        logger.error(f"Failed to connect to MQTT Broker: {MQTT_BROKER}, return code {rc}")

def on_disconnect(client, userdata, rc):
    """Callback when client disconnects from the MQTT broker."""
    logger.info(f"Disconnected from MQTT Broker with result code: {rc}")

def on_message(client, userdata, msg):
    """Callback when a message is received."""
    logger.info(f"Received message on topic: {msg.topic}")
    # We will handle message processing in specific topic subscriptions

def setup_mqtt_client():
    """
    Stub function for MQTT setup in demo mode.
    For a real implementation, this would initialize and connect to an MQTT broker.
    """
    logger.info("MQTT client setup skipped in demo mode")
    return True

def initialize_mqtt():
    """Initialize and connect to the MQTT broker (deprecated, use setup_mqtt_client instead)"""
    global mqtt_client
    
    if mqtt_client is not None:
        return mqtt_client
    
    # Create MQTT client
    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message = on_message
    
    # Connect to MQTT broker
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        # Start the loop in a separate thread
        mqtt_client.loop_start()
        logger.info("MQTT client initialized and connected")
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        mqtt_client = None
    
    return mqtt_client

def get_mqtt_client():
    """Get or initialize the MQTT client."""
    global mqtt_client
    if mqtt_client is None:
        mqtt_client = initialize_mqtt()
    return mqtt_client

def publish_message(topic, message, qos=1, retain=False):
    """
    Stub function for publishing messages in demo mode.
    In a real implementation, this would encrypt and publish messages to MQTT topics.
    """
    logger.info(f"Demo: Would publish message to {topic}")
    return True

def publish_multiple_messages(messages):
    """
    Stub function for publishing multiple messages in demo mode.
    In a real implementation, this would encrypt and publish messages to various MQTT topics.
    """
    logger.info(f"Demo: Would publish {len(messages)} messages")
    return True

def subscribe_to_topic(topic, callback=None, qos=1):
    """
    Stub function for subscribing to topics in demo mode.
    In a real implementation, this would set up subscription handlers for MQTT topics.
    """
    logger.info(f"Demo: Would subscribe to {topic}")
    return True

def unsubscribe_from_topic(topic):
    """
    Stub function for unsubscribing from topics in demo mode.
    In a real implementation, this would remove subscription handlers for MQTT topics.
    """
    logger.info(f"Demo: Would unsubscribe from {topic}")
    return True

def cleanup_mqtt():
    """
    Stub function for MQTT cleanup in demo mode.
    In a real implementation, this would disconnect from the MQTT broker.
    """
    logger.info("MQTT client cleanup skipped in demo mode")
    return True 