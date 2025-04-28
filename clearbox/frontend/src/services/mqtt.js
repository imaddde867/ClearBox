import mqtt from 'mqtt';
import { MQTT_CONFIG } from '../config';

let client = null;
let connectPromise = null;
let messageCallbacks = [];
let statusCallbacks = [];

// Initialize MQTT client
export const initializeMQTT = (userId, token) => {
  if (client) {
    console.log('MQTT client already initialized, disconnecting first');
    disconnectMQTT();
  }

  // Build connection options
  const options = {
    ...MQTT_CONFIG.OPTIONS,
    clientId: `clearbox_${userId}_${new Date().getTime()}`, // Ensure unique client ID
  };

  // Add auth token to options if available
  if (token) {
    options.properties = {
      ...options.properties,
      userProperties: {
        token
      }
    };
  }

  console.log(`Connecting to MQTT broker: ${MQTT_CONFIG.BROKER_URL}`);
  
  // Create client
  client = mqtt.connect(MQTT_CONFIG.BROKER_URL, options);

  // Setup event handlers
  connectPromise = new Promise((resolve, reject) => {
    const connectTimeout = setTimeout(() => {
      reject(new Error('MQTT connection timeout'));
    }, 10000); // 10 second timeout

    client.on('connect', () => {
      console.log('MQTT client connected');
      clearTimeout(connectTimeout);
      
      // Subscribe to user topic
      const userTopic = MQTT_CONFIG.TOPICS.USER_MESSAGES(userId);
      client.subscribe(userTopic, (err) => {
        if (err) {
          console.error(`Failed to subscribe to ${userTopic}:`, err);
        } else {
          console.log(`Subscribed to ${userTopic}`);
        }
      });

      // Notify status callbacks about connection
      statusCallbacks.forEach(callback => callback(true));
      
      resolve(client);
    });

    client.on('reconnect', () => {
      console.log('MQTT client reconnecting...');
    });

    client.on('error', (err) => {
      console.error('MQTT client error:', err);
      reject(err);
    });

    client.on('close', () => {
      console.log('MQTT connection closed');
      // Notify status callbacks about disconnect
      statusCallbacks.forEach(callback => callback(false));
    });

    client.on('message', (topic, message) => {
      try {
        // Try to parse message as JSON
        const data = JSON.parse(message.toString());
        console.log(`MQTT message received on topic ${topic}:`, data);
        
        // Pass to all registered callbacks
        messageCallbacks.forEach(callback => callback(topic, data));
      } catch (error) {
        console.error('Error processing MQTT message:', error);
        console.log('Raw message:', message.toString());
      }
    });
  });

  return connectPromise;
};

// Disconnect MQTT client
export const disconnectMQTT = () => {
  if (client && client.connected) {
    console.log('Disconnecting MQTT client');
    client.end();
  }
  client = null;
  connectPromise = null;
};

// Subscribe to a topic
export const subscribeTopic = async (topic) => {
  if (!client) {
    throw new Error('MQTT client not initialized');
  }

  try {
    // Wait for connection if not already connected
    if (connectPromise) {
      await connectPromise;
    }

    return new Promise((resolve, reject) => {
      client.subscribe(topic, (err) => {
        if (err) {
          console.error(`Failed to subscribe to ${topic}:`, err);
          reject(err);
        } else {
          console.log(`Subscribed to ${topic}`);
          resolve();
        }
      });
    });
  } catch (error) {
    console.error('Error subscribing to topic:', error);
    throw error;
  }
};

// Unsubscribe from a topic
export const unsubscribeTopic = async (topic) => {
  if (!client || !client.connected) {
    return;
  }

  return new Promise((resolve, reject) => {
    client.unsubscribe(topic, (err) => {
      if (err) {
        console.error(`Failed to unsubscribe from ${topic}:`, err);
        reject(err);
      } else {
        console.log(`Unsubscribed from ${topic}`);
        resolve();
      }
    });
  });
};

// Publish a message to a topic
export const publishMessage = async (topic, message) => {
  if (!client) {
    throw new Error('MQTT client not initialized');
  }

  try {
    // Wait for connection if not already connected
    if (connectPromise) {
      await connectPromise;
    }

    return new Promise((resolve, reject) => {
      // Convert to string if object
      const messageStr = typeof message === 'object' ? JSON.stringify(message) : message;
      
      client.publish(topic, messageStr, {}, (err) => {
        if (err) {
          console.error(`Failed to publish to ${topic}:`, err);
          reject(err);
        } else {
          console.log(`Published to ${topic}`);
          resolve();
        }
      });
    });
  } catch (error) {
    console.error('Error publishing message:', error);
    throw error;
  }
};

// Register a callback for incoming messages
export const onMessage = (callback) => {
  messageCallbacks.push(callback);
  return () => {
    messageCallbacks = messageCallbacks.filter(cb => cb !== callback);
  };
};

// Register a callback for connection status changes
export const onConnectionStatus = (callback) => {
  statusCallbacks.push(callback);
  // Initial callback if client exists
  if (client && client.connected) {
    callback(true);
  } else {
    callback(false);
  }
  return () => {
    statusCallbacks = statusCallbacks.filter(cb => cb !== callback);
  };
};

// Check if client is connected
export const isConnected = () => {
  return !!(client && client.connected);
};

// Get client instance (for advanced usage)
export const getClient = () => {
  return client;
};

export default {
  initializeMQTT,
  disconnectMQTT,
  subscribeTopic,
  unsubscribeTopic,
  publishMessage,
  onMessage,
  onConnectionStatus,
  isConnected,
  getClient
}; 