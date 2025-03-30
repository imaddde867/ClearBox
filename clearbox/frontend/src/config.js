/**
 * Application Configuration
 * This file contains environment-specific configuration
 */

// API configuration
const API_CONFIG = {
  // Base URL for API requests - uses environment variable or falls back to proxy in development
  BASE_URL: process.env.REACT_APP_API_URL || '',
  
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
  // MQTT broker URL - uses environment variable or falls back to dynamic location in production
  BROKER_URL: process.env.REACT_APP_MQTT_URL || 
    ((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + 
     window.location.host + '/mqtt'),
  
  // MQTT connection options
  OPTIONS: {
    keepalive: 30,
    connectTimeout: 10000,
    clean: true,
  },
  
  // Topic patterns
  TOPICS: {
    USER_MESSAGES: (userId) => `user/${userId}/messages`,
    GROUP_MESSAGES: (groupId) => `group/${groupId}/messages`,
    USER_STATUS: (userId) => `user/${userId}/status`,
  }
};

// Export the configuration objects
export { API_CONFIG, MQTT_CONFIG };
