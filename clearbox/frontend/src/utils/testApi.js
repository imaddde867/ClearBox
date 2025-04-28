import api from '../services/api';
import { API_CONFIG } from '../config';

/**
 * Enhanced utility to test API connectivity
 * Run this from the browser console with: testApiConnection()
 */
export async function testApiConnection() {
  console.log('====================================');
  console.log('Testing API connection...');
  console.log('====================================');
  console.log(`API Configuration: ${JSON.stringify(API_CONFIG, null, 2)}`);
  console.log(`Base URL: ${api.defaults.baseURL}`);
  
  // Check if in production
  console.log(`Environment: ${process.env.NODE_ENV}`);
  
  // Check token status
  const token = localStorage.getItem('token');
  console.log(`Auth Token: ${token ? 'Present' : 'Missing'}`);
  if (token) {
    try {
      // Basic token validation
      const parts = token.split('.');
      if (parts.length !== 3) {
        console.warn('⚠️ Token format is invalid (should have 3 parts separated by periods)');
      } else {
        const payload = JSON.parse(atob(parts[1]));
        console.log('Token payload:', payload);
        
        // Check expiration
        if (payload.exp) {
          const expDate = new Date(payload.exp * 1000);
          const now = new Date();
          console.log(`Token expires: ${expDate.toISOString()}`);
          console.log(`Current time: ${now.toISOString()}`);
          console.log(`Token ${expDate > now ? 'is valid' : 'has expired'}`);
        }
      }
    } catch (error) {
      console.error('Error parsing token:', error);
    }
  }

  try {
    // Try to access the root API endpoint
    console.log('\n------ Testing root API endpoint ------');
    try {
      const rootResponse = await api.get('/');
      console.log('✅ API root endpoint response:', rootResponse.status, rootResponse.data);
    } catch (error) {
      console.error('❌ API root endpoint error:', error.message);
      console.log('Response data:', error.response?.data);
      console.log('Status:', error.response?.status);
    }
  } catch (error) {
    console.error('❌ Failed to connect to API server:', error);
  }

  // Try specific API endpoints
  console.log('\n------ Testing critical endpoints ------');
  const endpoints = [
    { name: 'Login', method: 'post', path: API_CONFIG.ENDPOINTS.LOGIN, needsAuth: false, data: {} },
    { name: 'Register', method: 'post', path: API_CONFIG.ENDPOINTS.REGISTER, needsAuth: false, data: {} },
    { name: 'Profile', method: 'get', path: API_CONFIG.ENDPOINTS.PROFILE, needsAuth: true },
  ];

  for (const endpoint of endpoints) {
    try {
      console.log(`Testing ${endpoint.method.toUpperCase()} ${endpoint.path}...`);

      // Skip auth-required endpoints if no token present
      if (endpoint.needsAuth && !token) {
        console.log(`⚠️ Skipping ${endpoint.path} - requires authentication`);
        continue;
      }

      // Just checking if endpoint exists, not sending real data
      const options = {
        method: endpoint.method,
        url: endpoint.path,
      };

      // Only add data for POST/PUT, and use empty test data
      if (['post', 'put'].includes(endpoint.method)) {
        options.data = {};
      }

      // Modify the request to not actually send data for test
      try {
        // For POST/PUT requests, we'll just check OPTIONS to see if endpoint exists
        if (['post', 'put'].includes(endpoint.method)) {
          const response = await fetch(api.defaults.baseURL + endpoint.path, { method: 'OPTIONS' });
          console.log(`✅ ${endpoint.name}: ${endpoint.path} - Status ${response.status} ${response.ok ? '(Available)' : '(Error)'}`);
        } else {
          // For GET requests, we can use the API directly
          const response = await api.request(options);
          console.log(`✅ ${endpoint.name}: ${endpoint.path} - Status ${response.status} (Available)`);
        }
      } catch (error) {
        // Check if this is a 404 or a different error
        if (error.response && error.response.status === 404) {
          console.error(`❌ ${endpoint.name}: ${endpoint.path} - Endpoint not found (404)`);
        } else if (error.response) {
          // Other response error but endpoint exists
          console.log(`⚠️ ${endpoint.name}: ${endpoint.path} - Status ${error.response.status} (Available but error)`);
        } else {
          // Network or other error
          console.error(`❌ ${endpoint.name}: ${endpoint.path} - Error: ${error.message}`);
        }
      }
    } catch (error) {
      console.error(`❌ ${endpoint.path}: Error`, error);
    }
  }

  console.log('\n------ Network Connectivity Tests ------');
  // Test connectivity to the API domain 
  try {
    const apiUrl = API_CONFIG.BASE_URL || api.defaults.baseURL.replace('/api', '');
    console.log(`Testing connectivity to API domain: ${apiUrl}`);
    const response = await fetch(apiUrl, { method: 'HEAD' });
    console.log(`✅ API domain reachable: ${response.status}`);
  } catch (error) {
    console.error('❌ Cannot reach API domain:', error.message);
  }

  // Test CORS headers
  console.log('\nChecking CORS configuration...');
  try {
    const apiUrl = API_CONFIG.BASE_URL || api.defaults.baseURL;
    console.log(`Testing CORS on: ${apiUrl}`);
    const response = await fetch(apiUrl, { 
      method: 'OPTIONS',
      headers: {
        'Origin': window.location.origin,
      }
    });
    
    const corsHeaders = {
      'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
      'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
      'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
    };
    
    console.log('CORS Headers:', corsHeaders);
    if (corsHeaders['Access-Control-Allow-Origin']) {
      console.log('✅ CORS headers are present');
    } else {
      console.warn('⚠️ CORS headers are missing, which may cause issues with cross-origin requests');
    }
  } catch (error) {
    console.error('❌ Error checking CORS headers:', error.message);
  }

  console.log('\n====================================');
  console.log('Test complete. If you see errors:');
  console.log('1. Check that your backend server is running');
  console.log('2. Verify the API URL configuration');
  console.log('3. Check network connectivity and CORS settings');
  console.log('4. Examine backend logs for errors');
  console.log('====================================');
}

// Make it available globally for console testing
window.testApiConnection = testApiConnection;

// Additional utility to clear auth data and refresh
window.clearAuthAndRefresh = () => {
  console.log('Clearing auth data...');
  localStorage.removeItem('token');
  console.log('Auth data cleared. Refreshing page...');
  window.location.reload();
};

export default testApiConnection;