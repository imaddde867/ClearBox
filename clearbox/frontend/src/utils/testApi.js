import api from '../services/api';

/**
 * Simple utility to test API connectivity
 * Run this from the browser console with: testApiConnection()
 */
export async function testApiConnection() {
  console.log('Testing API connection...');

  try {
    // Try to access the root API endpoint
    const response = await fetch('/api');
    const status = response.status;
    console.log(`API connection test result: ${status}`);

    if (status >= 200 && status < 500) {
      console.log('✅ API server is reachable. Status:', status);
    } else {
      console.error('❌ API server returned error. Status:', status);
    }
  } catch (error) {
    console.error('❌ Failed to connect to API server:', error);
  }

  // Try specific API endpoints
  console.log('\nTesting specific endpoints:');
  const endpoints = [
    { method: 'get', url: '/api' },
    { method: 'get', url: '/api/profile', needsAuth: true },
  ];

  for (const endpoint of endpoints) {
    try {
      console.log(`Testing ${endpoint.method.toUpperCase()} ${endpoint.url}...`);

      // Skip auth-required endpoints if no token present
      if (endpoint.needsAuth && !localStorage.getItem('clearboxToken')) {
        console.log(`Skipping ${endpoint.url} - requires authentication`);
        continue;
      }

      const response = await fetch(endpoint.url, {
        method: endpoint.method,
        headers: {
          'Content-Type': 'application/json',
          ...(endpoint.needsAuth && localStorage.getItem('clearboxToken') ?
            { 'Authorization': `Bearer ${localStorage.getItem('clearboxToken')}` } : {})
        }
      });

      console.log(`${endpoint.url}: Status ${response.status}`);
    } catch (error) {
      console.error(`${endpoint.url}: Error`, error);
    }
  }

  console.log('\nTest complete. If you see errors, check that your backend server is running at http://localhost:8000');
}

// Make it available globally for console testing
window.testApiConnection = testApiConnection;

export default testApiConnection;