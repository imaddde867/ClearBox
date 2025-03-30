import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState(null);
  const [authStatus, setAuthStatus] = useState('idle');

  // Add a validation function to check if token exists and is valid
  const validateToken = () => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.warn('validateToken: No token found in localStorage');
      return false;
    }

    try {
      // Basic validation - check if token has three parts (header.payload.signature)
      const parts = token.split('.');
      if (parts.length !== 3) {
        console.warn('validateToken: Token format is invalid');
        return false;
      }

      // Try to decode the payload (middle part)
      const payload = JSON.parse(atob(parts[1]));

      // Check if token is expired
      if (payload.exp && payload.exp * 1000 < Date.now()) {
        console.warn('validateToken: Token is expired');
        localStorage.removeItem('token');
        return false;
      }

      return true;
    } catch (error) {
      console.error('validateToken: Error validating token', error);
      return false;
    }
  };

  // Replace the current token check in useEffect with the validation
  useEffect(() => {
    const isValid = validateToken();
    if (isValid) {
      console.log('Auth token found and validated, loading user profile...');
      loadUserProfile();
    } else {
      console.log('No valid auth token found, skipping profile load');
      setLoading(false);
    }

    // Listen for auth error events (from API interceptor)
    const handleAuthError = (event) => {
      console.log('Auth error received:', event.detail.message);
      setAuthError(event.detail.message);
      setCurrentUser(null);
    };

    window.addEventListener('auth:error', handleAuthError);

    return () => {
      window.removeEventListener('auth:error', handleAuthError);
    };
  }, []);

  const loadUserProfile = async () => {
    try {
      setAuthStatus('loading');
      setLoading(true);
      console.log('Fetching user profile...');
      const response = await api.get('/profile');
      console.log('Profile loaded successfully');
      setCurrentUser(response.data);
      setAuthStatus('success');
    } catch (error) {
      console.error('Failed to load user profile:', error);
      localStorage.removeItem('token');
      setAuthError('Session expired. Please login again.');
      setAuthStatus('error');
    } finally {
      setLoading(false);
    }
  };

  // Add function to update user profile
  const updateProfile = async (userData) => {
    try {
      setAuthStatus('loading');
      setLoading(true);

      // Use PUT method to match the backend endpoint
      const response = await api.put('/users/me', userData);

      // Update the current user state with the response data
      setCurrentUser(response.data);

      setAuthStatus('success');
      return response.data;
    } catch (error) {
      console.error('Profile update error:', error);
      setAuthError(error.response?.data?.detail || 'Failed to update profile');
      setAuthStatus('error');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signup = async (username, email, password, consentData = {}) => {
    try {
      setAuthStatus('loading');
      setLoading(true);

      // Include the consent data in signup
      const signupData = {
        username,
        email,
        password,
        ...consentData
      };

      console.log('Signing up new user...');
      const response = await api.post('/register', signupData);
      console.log('Signup successful, saving token');

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        await loadUserProfile();
      } else {
        console.error('No token received during signup');
        throw new Error('Authentication failed: No token received');
      }

      setAuthStatus('success');
      return response.data;
    } catch (error) {
      console.error('Signup error:', error);
      setAuthError(error.response?.data?.detail || 'Failed to create account');
      setAuthStatus('error');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const login = async (usernameOrEmail, password) => {
    try {
      setAuthStatus('loading');
      setLoading(true);

      console.log('Logging in user...');
      // Use the /login/email endpoint instead to send JSON
      const response = await api.post('/login/email', {
        email: usernameOrEmail,
        password: password
      });

      console.log('Login successful, saving token');
      if (response.data.access_token) {
        // Store token in localStorage with consistent key
        localStorage.setItem('token', response.data.access_token);

        // Double-check that token was saved correctly
        const savedToken = localStorage.getItem('token');
        if (!savedToken) {
          console.error('Token was not properly saved to localStorage');
          throw new Error('Authentication failed: Could not save token');
        }

        await loadUserProfile();
      } else {
        console.error('No token received during login');
        throw new Error('Authentication failed: No token received');
      }

      setAuthStatus('success');
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      setAuthError(error.response?.data?.detail || 'Failed to login');
      setAuthStatus('error');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setCurrentUser(null);
    setAuthStatus('idle');
    console.log('User logged out successfully');
  };

  const isAuthenticated = () => {
    return !!currentUser && validateToken();
  };

  const value = {
    currentUser,
    loading,
    authError,
    authStatus,
    login,
    signup,
    logout,
    updateProfile,
    isAuthenticated
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}