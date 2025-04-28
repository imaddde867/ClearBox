/**
 * Application Configuration
 */

// API configuration
const API_CONFIG = {
  // Base URL for API requests - uses environment variable or falls back to api subdomain
  BASE_URL: process.env.REACT_APP_API_URL || 'https://api.clearbox.live',
  
  // API endpoints
  ENDPOINTS: {
    LOGIN: '/api/login',
    SIGNUP: '/api/signup',
    PROFILE: '/api/profile',
    CONTACTS: '/api/contacts',
    CONTACT_REQUEST: '/api/contact/request',
    CONTACT_REQUESTS: '/api/contact/requests',
    CONTACT_ACCEPT: '/api/contact/accept',
    CONTACT_DENY: '/api/contact/deny',
    SEARCH: '/api/search',
    MESSAGES: '/api/messages',
    MESSAGES_USER: (userId) => `/api/messages/user/${userId}`,
    MESSAGES_GROUP: (groupId) => `/api/messages/group/${groupId}`,
    MESSAGE_DELIVERED: (messageId) => `/api/messages/${messageId}/delivered`,
    MESSAGE_READ: (messageId) => `/api/messages/${messageId}/read`,
    GROUPS: '/api/groups',
    GROUP: (groupId) => `/api/group/${groupId}`,
    GROUP_CREATE: '/api/group',
    GROUP_ADD: (groupId) => `/api/group/${groupId}/add`,
    NOTIFICATIONS: '/api/notifications',
  }
};

// MQTT configuration
const MQTT_CONFIG = {
  // MQTT broker URL - use environment variable or default
  BROKER_URL: process.env.REACT_APP_MQTT_URL || 
    (process.env.NODE_ENV === 'production' 
      ? 'wss://beb6c3d91a0e4befbb836d5269d627ea.s1.eu.hivemq.cloud:8884/mqtt'
      : 'ws://localhost:9001'),
  
  // MQTT connection options
  OPTIONS: {
    keepalive: 30,
    connectTimeout: 10000,
    clean: true,
    // For production HiveMQ connection
    ...(process.env.NODE_ENV === 'production' && {
      username: process.env.REACT_APP_MQTT_USERNAME || 'imadeddine200507',
      password: process.env.REACT_APP_MQTT_PASSWORD || '120705Imad',
      ssl: true,
      protocolVersion: 5
    })
  },
  
  // Topic patterns
  TOPICS: {
    USER_MESSAGES: (userId) => `user/${userId}/messages`,
    GROUP_MESSAGES: (groupId) => `group/${groupId}/messages`,
    USER_STATUS: (userId) => `user/${userId}/status`,
  }
};

// Check environment
if (process.env.NODE_ENV === 'production') {
  console.log('Running in production mode');
  console.log(`API URL: ${API_CONFIG.BASE_URL}`);
  console.log(`MQTT Broker: ${MQTT_CONFIG.BROKER_URL}`);
} else {
  console.log('Running in development mode');
}

// Export the configuration objects
export { API_CONFIG, MQTT_CONFIG };
