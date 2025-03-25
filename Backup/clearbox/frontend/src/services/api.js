import axios from 'axios';

// Create a custom instance of axios with default configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Direct connection to backend instead of relying on proxy
  headers: {
    'Content-Type': 'application/json',
  },
  // Add timeout to prevent hanging requests
  timeout: 10000, // 10 seconds
});

// Function to log token availability - for debugging
const logTokenStatus = () => {
  const token = localStorage.getItem('clearboxToken');
  console.log(`Token status: ${token ? 'Present' : 'Missing'} - ${new Date().toISOString()}`);
};

// Add request logging for debugging
const logRequestDetails = (config) => {
  console.log(`API Request:
    URL: ${config.baseURL}${config.url}
    Method: ${config.method.toUpperCase()}
    Headers: ${JSON.stringify(config.headers)}
    Timestamp: ${new Date().toISOString()}
  `);
  
  if (config.method !== 'get') {
    console.log(`Request data: ${JSON.stringify(config.data || {})}`);
  }
  
  return config;
};

// Add a request interceptor to include the token in all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('clearboxToken');
    
    // For debugging purposes
    if (config.url.includes('/messages') || config.url.includes('/contact')) {
      console.log(`API Request to ${config.url} - Token: ${token ? 'Present' : 'Missing'}`);
    }
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      console.warn(`API Request to ${config.url} - No authentication token available`);
    }
    
    // Log full request details for debugging
    return logRequestDetails(config);
  },
  (error) => {
    console.error('API Request Interceptor Error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    // Log successful responses for debugging
    console.log(`API Response Success: ${response.config.url} - Status: ${response.status}`);
    return response;
  },
  (error) => {
    // First check if it's a network error (no response)
    if (error.message === 'Network Error') {
      console.error('Network error detected. Server may be down or unreachable.');
      console.log('Browser network status:', navigator.onLine ? 'Online' : 'Offline');
      
      // Try to diagnose the issue
      fetch(error.config?.baseURL || 'http://localhost:8000')
        .then(response => {
          console.log('Server ping test - response:', response.status);
        })
        .catch(pingError => {
          console.error('Server ping test failed:', pingError);
        });
    }
    
    // You can handle specific error statuses here
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('API Error:', error.response.status, error.response.data, 
                    'URL:', error.config?.url, 'Method:', error.config?.method);
      
      if (error.response.status === 401) {
        // Unauthorized - clear token and flag for re-authentication
        console.error('Authentication token expired or invalid. Clearing token.');
        localStorage.removeItem('clearboxToken');
        
        // Emit an event for handling expired sessions
        const authErrorEvent = new CustomEvent('auth:error', { 
          detail: { message: 'Session expired. Please log in again.' }
        });
        window.dispatchEvent(authErrorEvent);
        
        // After 2 seconds, redirect to login page (gives time for event handlers)
        setTimeout(() => {
          if (window.location.pathname !== '/login') {
            window.location.href = '/login';
          }
        }, 2000);
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('API Request Error - No response received:', error.request);
      console.error('Request details:', {
        url: error.config?.url,
        method: error.config?.method,
        baseURL: error.config?.baseURL,
        timeout: error.config?.timeout,
        headers: error.config?.headers
      });
      
      // Check if it's a timeout
      if (error.code === 'ECONNABORTED') {
        console.error('Request timed out. The server may be under heavy load or unreachable.');
      }
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('API Setup Error:', error.message);
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

// Start by checking if token is available (helps with debugging)
logTokenStatus();

// Export the API service and utilities
export default api; 