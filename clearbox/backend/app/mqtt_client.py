import paho.mqtt.client as mqtt
from paho.mqtt.publish import multiple
import json
import os
import logging
import ssl
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
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

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
    """Set up and connect to the MQTT broker."""
    global mqtt_client
    
    if ENVIRONMENT == "development":
        logger.info("Development mode: Using demo MQTT setup")
        return True
    
    # If we already have a client, return it
    if mqtt_client is not None:
        return mqtt_client

    # Create MQTT client
    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message = on_message

    # Set up authentication if provided
    if MQTT_USERNAME and MQTT_PASSWORD:
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        logger.info("MQTT authentication configured")

    # Set up TLS if enabled (required for production)
    if MQTT_USE_TLS:
        try:
            # Configure TLS with server certificate verification
            mqtt_client.tls_set(
                ca_certs=None,  # Set to path of CA certificate for verification in production
                certfile=None,  # Client certificate for mutual TLS (optional)
                keyfile=None,   # Client key for mutual TLS (optional)
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None
            )
            # Don't verify hostname in development, but do in production
            mqtt_client.tls_insecure_set(ENVIRONMENT != "production")
            logger.info("MQTT TLS configured")
        except Exception as e:
            logger.error(f"Failed to configure TLS for MQTT: {e}")
            return False

    # Connect to MQTT broker
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        # Start the loop in a separate thread
        mqtt_client.loop_start()
        logger.info("MQTT client initialized and connected")
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        mqtt_client = None
        return False

    return mqtt_client

def get_mqtt_client():
    """Get or initialize the MQTT client."""
    global mqtt_client
    if mqtt_client is None:
        mqtt_client = setup_mqtt_client()
    return mqtt_client

def publish_message(topic, message, qos=1, retain=False):
    """Publish a message to an MQTT topic."""
    if ENVIRONMENT == "development":
        logger.info(f"Demo: Would publish message to {topic}")
        return True
    
    client = get_mqtt_client()
    if not client:
        logger.error("MQTT client not available for publishing")
        return False
    
    try:
        if isinstance(message, dict):
            message = json.dumps(message)
        
        # In production, you'd encrypt the message here
        # message = encrypt_message(message)
        
        result = client.publish(topic, message, qos=qos, retain=retain)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            logger.error(f"Failed to publish message to {topic}: {result}")
            return False
        
        logger.info(f"Message published to {topic}")
        return True
    except Exception as e:
        logger.error(f"Error publishing message to {topic}: {e}")
        return False

def publish_multiple_messages(messages):
    """Publish multiple messages to various MQTT topics."""
    if ENVIRONMENT == "development":
        logger.info(f"Demo: Would publish {len(messages)} messages")
        return True
    
    if not messages:
        return True
    
    try:
        # Format messages for paho-mqtt's multiple() function
        formatted_messages = []
        for msg in messages:
            topic = msg.get("topic")
            payload = msg.get("message")
            qos = msg.get("qos", 1)
            retain = msg.get("retain", False)
            
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            
            # In production, you'd encrypt the payload here
            # payload = encrypt_message(payload)
            
            formatted_messages.append({
                "topic": topic,
                "payload": payload,
                "qos": qos,
                "retain": retain
            })
        
        auth = None
        if MQTT_USERNAME and MQTT_PASSWORD:
            auth = {"username": MQTT_USERNAME, "password": MQTT_PASSWORD}
        
        multiple(formatted_messages, hostname=MQTT_BROKER, port=MQTT_PORT, auth=auth)
        logger.info(f"Published {len(formatted_messages)} messages")
        return True
    except Exception as e:
        logger.error(f"Error publishing multiple messages: {e}")
        return False

def subscribe_to_topic(topic, callback=None, qos=1):
    """Subscribe to an MQTT topic."""
    if ENVIRONMENT == "development":
        logger.info(f"Demo: Would subscribe to {topic}")
        return True
    
    client = get_mqtt_client()
    if not client:
        logger.error("MQTT client not available for subscribing")
        return False
    
    try:
        if callback:
            client.message_callback_add(topic, callback)
        
        result = client.subscribe(topic, qos)
        if result[0] != mqtt.MQTT_ERR_SUCCESS:
            logger.error(f"Failed to subscribe to {topic}: {result}")
            return False
        
        logger.info(f"Subscribed to {topic} with QoS {qos}")
        return True
    except Exception as e:
        logger.error(f"Error subscribing to {topic}: {e}")
        return False

def unsubscribe_from_topic(topic):
    """Unsubscribe from an MQTT topic."""
    if ENVIRONMENT == "development":
        logger.info(f"Demo: Would unsubscribe from {topic}")
        return True
    
    client = get_mqtt_client()
    if not client:
        logger.error("MQTT client not available for unsubscribing")
        return False
    
    try:
        result = client.unsubscribe(topic)
        if result[0] != mqtt.MQTT_ERR_SUCCESS:
            logger.error(f"Failed to unsubscribe from {topic}: {result}")
            return False
        
        logger.info(f"Unsubscribed from {topic}")
        return True
    except Exception as e:
        logger.error(f"Error unsubscribing from {topic}: {e}")
        return False

def cleanup_mqtt():
    """Clean up MQTT resources before shutdown."""
    global mqtt_client
    
    if ENVIRONMENT == "development":
        logger.info("MQTT client cleanup skipped in demo mode")
        return True
    
    if mqtt_client is None:
        return True
    
    try:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        logger.info("MQTT client disconnected")
        mqtt_client = None
        return True
    except Exception as e:
        logger.error(f"Error during MQTT cleanup: {e}")
        return False