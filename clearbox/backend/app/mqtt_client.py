import paho.mqtt.client as mqtt
from paho.mqtt.publish import multiple
import json
import os
import logging
import ssl
import time
import threading
from dotenv import load_dotenv
#from .encryption import encrypt_message, decrypt_message
import socket

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = 120  # Increased from 60 to 120 seconds
MQTT_CLIENT_ID = f"clearbox_server_{int(time.time())}"  # Add timestamp to make ID unique
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)
MQTT_USE_SSL = os.getenv("MQTT_USE_SSL", "false").lower() == "true"
# Reconnection parameters
MQTT_RECONNECT_DELAY = 5  # seconds between reconnection attempts
# Keep-alive topic
MQTT_KEEPALIVE_TOPIC = "clearbox/server/keepalive"
MQTT_KEEPALIVE_INTERVAL = 30  # Increased from 5 to 30 seconds

# Global client instance
mqtt_client = None
keep_alive_timer = None
is_connected = False
reconnect_count = 0  # Track reconnection attempts

def send_keepalive():
    """Send a keep-alive message periodically to maintain the connection"""
    global keep_alive_timer, is_connected
    
    if not is_connected:
        logger.debug("Not sending keep-alive because not connected")
        return
    
    try:
        # Publish a keep-alive message
        if mqtt_client:
            result = mqtt_client.publish(
                MQTT_KEEPALIVE_TOPIC, 
                json.dumps({"timestamp": time.time(), "status": "alive"}),
                qos=0,  # Use QoS 0 for keepalive to reduce overhead
                retain=False
            )
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug("Keep-alive message sent successfully")
            else:
                logger.warning(f"Failed to send keep-alive message, result: {result.rc}")
    except Exception as e:
        logger.error(f"Error sending keep-alive message: {e}")
    
    # Schedule the next keep-alive
    keep_alive_timer = threading.Timer(MQTT_KEEPALIVE_INTERVAL, send_keepalive)
    keep_alive_timer.daemon = True
    keep_alive_timer.start()

def on_connect(client, userdata, flags, rc):
    """Callback when client connects to the MQTT broker."""
    global is_connected, reconnect_count
    
    if rc == 0:
        logger.info(f"Connected to MQTT Broker: {MQTT_BROKER}")
        # Reset reconnect counter on successful connection
        reconnect_count = 0
        is_connected = True
        
        # Subscribe to the server topics
        client.subscribe(f"clearbox/server/#", qos=1)
        
        # Start sending keep-alive messages after a short delay
        threading.Timer(2.0, send_keepalive).start()
    else:
        is_connected = False
        error_messages = {
            1: "Connection refused - incorrect protocol version",
            2: "Connection refused - invalid client identifier",
            3: "Connection refused - server unavailable",
            4: "Connection refused - bad username or password",
            5: "Connection refused - not authorized"
        }
        error_msg = error_messages.get(rc, f"Unknown error code: {rc}")
        logger.error(f"Failed to connect to MQTT Broker: {MQTT_BROKER}, {error_msg}")

def on_disconnect(client, userdata, rc):
    """Callback when client disconnects from the MQTT broker."""
    global is_connected, reconnect_count
    
    is_connected = False
    logger.info(f"Disconnected from MQTT Broker with result code: {rc}")
    
    # Cancel any pending keep-alive
    if keep_alive_timer:
        keep_alive_timer.cancel()
    
    # If this is an unexpected disconnect, attempt to reconnect
    if rc != 0:
        # Protocol error 7 is common with HiveMQ - log more details
        if rc == 7:
            logger.warning("Disconnected with protocol error (code 7). This might be due to packet size, connection limits, or network issues.")
        else:
            logger.warning(f"Unexpected disconnection with code {rc}, will attempt to reconnect")
        
        # Increment reconnect counter
        reconnect_count += 1
        
        # Use exponential backoff for reconnection attempts
        reconnect_delay = min(MQTT_RECONNECT_DELAY * (2 ** min(reconnect_count - 1, 4)), 60)  # Cap at 60 seconds
        logger.info(f"Attempting reconnection in {reconnect_delay} seconds (attempt {reconnect_count})")
        
        # Don't block the callback thread, schedule reconnection
        threading.Timer(reconnect_delay, reconnect_client).start()

def reconnect_client():
    """Attempt to reconnect the MQTT client"""
    global mqtt_client
    
    if mqtt_client is None:
        logger.error("Cannot reconnect: MQTT client is None")
        return
        
    try:
        # If too many reconnection attempts, recreate the client
        if reconnect_count > 5:
            logger.info("Too many reconnection attempts, recreating MQTT client")
            cleanup_mqtt()
            setup_mqtt_client()
        else:
            logger.info("Attempting to reconnect existing client")
            mqtt_client.reconnect()
    except Exception as e:
        logger.error(f"Failed to reconnect: {e}")
        # Schedule another attempt
        threading.Timer(MQTT_RECONNECT_DELAY, reconnect_client).start()

def on_message(client, userdata, msg):
    """Callback when a message is received."""
    logger.info(f"Received message on topic: {msg.topic}")
    # We will handle message processing in specific topic subscriptions

def setup_mqtt_client():
    """Set up and connect to the MQTT broker."""
    global mqtt_client
    
    # If we already have a client, clean it up first
    if mqtt_client is not None:
        try:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        except:
            pass  # Ignore errors during cleanup

    # Create MQTT client with clean session=True to avoid stale session data
    # This helps with protocol errors when reconnecting
    mqtt_client = mqtt.Client(
        client_id=MQTT_CLIENT_ID, 
        clean_session=True,
        protocol=mqtt.MQTTv311  # Explicitly use v3.1.1 protocol
    )
    
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message = on_message
    
    # Set up automatic reconnect options - disabled in favor of our custom reconnect
    mqtt_client.reconnect_delay_set(min_delay=1, max_delay=60)
    
    # Disable the paho-mqtt automatic reconnect to use our own implementation
    mqtt_client.reconnect_delay_set(min_delay=1, max_delay=1)  # Minimal delay
    mqtt_client._reconnect_on_failure = False

    # Set up authentication if provided
    if MQTT_USERNAME and MQTT_PASSWORD:
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        logger.info("MQTT authentication configured")
    
    # Configure SSL/TLS if enabled
    if MQTT_USE_SSL:
        try:
            # Use a more specific SSL context with modern ciphers
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            mqtt_client.tls_set_context(context)
            # Set additional TLS options to prevent protocol errors
            mqtt_client.tls_insecure_set(False)
            logger.info("MQTT SSL/TLS configured with secure defaults")
        except Exception as e:
            logger.error(f"Error configuring TLS: {e}")
            # Fallback to basic TLS setup
            mqtt_client.tls_set(
                certfile=None,
                keyfile=None,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None
            )
            logger.info("MQTT SSL/TLS configured with fallback options")

    # Connect to MQTT broker
    try:
        # Set socket options to prevent network errors
        mqtt_client.socket_options = (
            (socket.SOL_TCP, socket.TCP_NODELAY, 1),  # Disable Nagle's algorithm
            (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # Enable TCP keepalive
        )
        
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
    client = get_mqtt_client()
    if not client:
        logger.error("MQTT client not available for publishing")
        return False
    
    try:
        if isinstance(message, dict):
            message = json.dumps(message)
        
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
            
            formatted_messages.append({
                "topic": topic,
                "payload": payload,
                "qos": qos,
                "retain": retain
            })
        
        auth = None
        if MQTT_USERNAME and MQTT_PASSWORD:
            auth = {"username": MQTT_USERNAME, "password": MQTT_PASSWORD}
        
        # Add TLS config for multiple() call if needed
        tls = None
        if MQTT_USE_SSL:
            tls = {'cert_reqs': ssl.CERT_REQUIRED, 
                   'tls_version': ssl.PROTOCOL_TLS}
        
        multiple(formatted_messages, hostname=MQTT_BROKER, port=MQTT_PORT, auth=auth, tls=tls)
        logger.info(f"Published {len(formatted_messages)} messages")
        return True
    except Exception as e:
        logger.error(f"Error publishing multiple messages: {e}")
        return False

def subscribe_to_topic(topic, callback=None, qos=1):
    """Subscribe to an MQTT topic."""
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
    global mqtt_client, keep_alive_timer
    
    # Cancel any pending keep-alive
    if keep_alive_timer:
        keep_alive_timer.cancel()
    
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