import axios from 'axios';

// Create an axios instance with a base URL and common settings
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  // Increase timeout to prevent timeout errors
  timeout: 30000, // Increase from default 10000ms to 30000ms (30 seconds)
  headers: {
    'Content-Type': 'application/json',
  }
});

// Function to log token availability - for debugging
const logTokenStatus = () => {
  const token = localStorage.getItem('token');
  console.log(`Token status: ${token ? 'Present' : 'Missing'} - ${new Date().toISOString()}`);
};

// Add request logging for debugging
const logRequestDetails = (config) => {
  // More detailed logging for message-related endpoints
  const isMessageEndpoint = config.url.includes('/messages');
  
  if (isMessageEndpoint) {
    console.log(`MESSAGE API Request:
      URL: ${config.baseURL}${config.url}
      Method: ${config.method.toUpperCase()}
      Headers: ${JSON.stringify(config.headers)}
      Timestamp: ${new Date().toISOString()}
      Data: ${config.method !== 'get' ? JSON.stringify(config.data || {}) : 'GET request (no data)'}
    `);
  }
  
  return config;
};

// Add a request interceptor to include the authentication token with each request
api.interceptors.request.use(
  config => {
    // Check if a token exists in local storage
    const token = localStorage.getItem('token');
    console.log('Token status:', token ? 'Found' : 'Missing', '-', new Date().toISOString());
    
    // If the token exists, add it to the Authorization header
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Log extra details for message endpoints
    if (config.url.includes('/messages')) {
      return logRequestDetails(config);
    }
    
    return config;
  },
  error => {
    // Do something with request error
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle common error cases
api.interceptors.response.use(
  response => {
    // Log successful message responses
    if (response.config.url.includes('/messages')) {
      console.log(`Message API Success:
        URL: ${response.config.url}
        Status: ${response.status}
        Data: ${JSON.stringify(response.data)}
      `);
    }
    
    // Any status code within the range of 2xx triggers this function
    return response;
  },
  error => {
    // Any status codes outside the range of 2xx trigger this function
    if (error.code === 'ECONNABORTED') {
      console.error('Request timed out. The server may be under heavy load or unreachable.');
    } else if (!error.response) {
      console.error('No response received:', error);
      console.error('Request details:', error.config);
      console.error('Request timed out. The server may be under heavy load or unreachable.');
    } else if (error.response.status === 401) {
      // Handle 401 Unauthorized errors
      console.error('Authentication error. You may need to log in again.');
      // Clear token if it's invalid
      localStorage.removeItem('token');
    } else if (error.response.status === 403) {
      // Handle 403 Forbidden errors
      console.error('You do not have permission to access this resource.');
    } else if (error.response.status === 404) {
      // Handle 404 Not Found errors
      console.error(`Resource not found: ${error.config.url}`);
      if (error.config.url.includes('/messages')) {
        console.error('Message endpoint not found. Check if the API endpoint is correct.');
      }
    } else if (error.response.status === 500) {
      // Handle 500 Internal Server Error
      console.error('Server error. Please try again later or contact support.');
    }
    
    return Promise.reject(error);
  }
);

// Function to test connectivity to the backend
export const testBackendConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api');
    return {
      status: response.status,
      ok: response.ok,
      statusText: response.statusText
    };
  } catch (error) {
    return {
      error: error.message,
      status: 'failed'
    };
  }
};

// Helper function to print available API endpoints - helps debugging
export const debugApiEndpoints = () => {
  // This is just a list of expected endpoints based on your code
  const expectedEndpoints = [
    '/login',
    '/register',
    '/profile',
    '/messages',
    '/messages/user/{userId}',
    '/contacts',
    '/contacts/requests'
  ];
  
  console.log('Expected API endpoints:');
  expectedEndpoints.forEach(endpoint => {
    console.log(`- ${endpoint}`);
  });
  
  console.log('To debug 404 errors, check if these endpoints match your backend implementation.');
};

// Start by checking if token is available (helps with debugging)
logTokenStatus();
debugApiEndpoints();

// Export the API service and utilities
export default api; 