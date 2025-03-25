import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from './AuthContext';

const ContactsContext = createContext();

export function useContacts() {
  return useContext(ContactsContext);
}

export function ContactsProvider({ children }) {
  const { currentUser } = useAuth();
  const [contacts, setContacts] = useState([]);
  const [contactRequests, setContactRequests] = useState([]);
  const [sentRequests, setSentRequests] = useState([]);
  // Use separate loading states for different data types
  const [contactsLoading, setContactsLoading] = useState(false);
  const [requestsLoading, setRequestsLoading] = useState(false);
  const [sentRequestsLoading, setSentRequestsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);

  // Use refs to track data loaded state
  const contactsLoadedRef = React.useRef(false);
  const requestsLoadedRef = React.useRef(false);
  const sentRequestsLoadedRef = React.useRef(false);

  // Set up polling for contacts when user logs in
  useEffect(() => {
    if (!currentUser) return;

    // Initial load
    loadContacts();
    loadContactRequests();
    loadSentRequests();

    // Set up polling every 10 seconds
    const pollInterval = setInterval(() => {
      // Use silent background refreshes for polling
      if (contactsLoadedRef.current) {
        loadContacts(true); // silent refresh
      }
      if (requestsLoadedRef.current) {
        loadContactRequests(true); // silent refresh
      }
      if (sentRequestsLoadedRef.current) {
        loadSentRequests(true); // silent refresh
      }
    }, 10000);

    return () => {
      clearInterval(pollInterval);
    };
  }, [currentUser]);

  const loadContacts = async (silent = false) => {
    if (!currentUser) return;

    // Only show loading state if it's not a silent refresh and data hasn't been loaded yet
    if (!silent && !contactsLoadedRef.current) {
      setContactsLoading(true);
    }

    try {
      console.log('Loading contacts...');
      const response = await api.get('/contacts');

      // Compare if the contacts actually changed to avoid unnecessary rerenders
      const newContacts = response.data;
      const currentContactIds = contacts.map(c => c.id).sort().join(',');
      const newContactIds = newContacts.map(c => c.id).sort().join(',');

      // Only update state if contacts changed
      if (currentContactIds !== newContactIds) {
        console.log('Contacts updated, setting new state');
        setContacts(newContacts);
      } else {
        console.log('Contacts unchanged, skipping state update');
      }

      // Mark as loaded regardless of content to prevent infinite loading
      contactsLoadedRef.current = true;
      setError(null);
    } catch (err) {
      console.error('Failed to load contacts:', err);
      // Only show errors for non-silent refreshes
      if (!silent) {
        setError('Failed to load contacts. Please try again.');
      }
    } finally {
      // Always ensure we turn off loading when done to prevent infinite loading states
      setContactsLoading(false);
    }
  };

  const loadContactRequests = async (silent = false) => {
    if (!currentUser) return;

    // Only show loading state if it's not a silent refresh and data hasn't been loaded yet
    if (!silent && !requestsLoadedRef.current) {
      setRequestsLoading(true);
    }

    try {
      console.log('Loading contact requests...');
      const response = await api.get('/contacts/requests');

      // Compare if the requests actually changed to avoid unnecessary rerenders
      const newRequests = response.data;
      const currentRequestIds = contactRequests.map(r => r.id).sort().join(',');
      const newRequestIds = newRequests.map(r => r.id).sort().join(',');

      // Only update state if requests changed
      if (currentRequestIds !== newRequestIds) {
        console.log('Contact requests updated, setting new state');
        setContactRequests(newRequests);
      } else {
        console.log('Contact requests unchanged, skipping state update');
      }

      // Mark as loaded regardless of content to prevent infinite loading
      requestsLoadedRef.current = true;
      setError(null);
    } catch (err) {
      console.error('Failed to load contact requests:', err);
      // Only show errors for non-silent refreshes
      if (!silent) {
        setError('Failed to load contact requests. Please try again.');
      }
    } finally {
      // Always ensure we turn off loading when done
      setRequestsLoading(false);
    }
  };

  const loadSentRequests = async (silent = false) => {
    if (!currentUser) return;

    // Only show loading state if it's not a silent refresh and data hasn't been loaded yet
    if (!silent && !sentRequestsLoadedRef.current) {
      setSentRequestsLoading(true);
    }

    try {
      console.log('Loading sent requests...');
      const response = await api.get('/contacts/sent-requests');

      // Compare if the sent requests actually changed to avoid unnecessary rerenders
      const newSentRequests = response.data;
      const currentSentIds = sentRequests.map(r => r.id).sort().join(',');
      const newSentIds = newSentRequests.map(r => r.id).sort().join(',');

      // Only update state if sent requests changed
      if (currentSentIds !== newSentIds) {
        console.log('Sent requests updated, setting new state');
        setSentRequests(newSentRequests);
      } else {
        console.log('Sent requests unchanged, skipping state update');
      }

      // Mark as loaded regardless of content to prevent infinite loading
      sentRequestsLoadedRef.current = true;
      setError(null);
    } catch (err) {
      console.error('Failed to load sent requests:', err);
      // Only show errors for non-silent refreshes
      if (!silent) {
        setError('Failed to load sent requests. Please try again.');
      }
    } finally {
      // Always ensure we turn off loading when done
      setSentRequestsLoading(false);
    }
  };

  const searchUsers = async (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    setSearchLoading(true);
    try {
      const response = await api.get(`/users/search?q=${encodeURIComponent(query)}`);
      // Filter out current user and existing contacts from search results
      const filteredResults = response.data.filter(user =>
        user.id !== currentUser?.id &&
        !contacts.some(contact => contact.id === user.id)
      );
      setSearchResults(filteredResults);
      setError(null);
    } catch (err) {
      console.error('Failed to search users:', err);
      setError('Failed to search users. Please try again.');
    } finally {
      setSearchLoading(false);
    }
  };

  const sendContactRequest = async (userId) => {
    setSentRequestsLoading(true);
    try {
      await api.post(`/contacts/request/${userId}`);
      // Refresh sent requests after sending a new one
      await loadSentRequests();
      setError(null);
      return { success: true };
    } catch (err) {
      console.error('Failed to send contact request:', err);

      // Get the specific error message from the API response
      const errorMessage = err.response?.data?.detail || 'Failed to send contact request. Please try again.';

      // Set a more specific error message based on the API response
      setError(errorMessage);

      // Return the error details so the component can show the specific error
      return {
        success: false,
        message: errorMessage,
        error: err
      };
    } finally {
      setSentRequestsLoading(false);
    }
  };

  const acceptContactRequest = async (requestId) => {
    setRequestsLoading(true);
    try {
      console.log(`Accepting contact request with ID: ${requestId}`);

      // Try the first endpoint format - with request_id
      try {
        await api.post(`/contacts/accept/${requestId}`);
      } catch (firstAttemptError) {
        console.log('First attempt failed, trying alternative endpoint format');

        // If that fails, try the alternative endpoint format
        await api.post(`/contact/accept/${requestId}`);
      }

      console.log('Contact request accepted successfully');

      // Refresh contacts and requests after accepting
      try {
        await Promise.all([
          loadContacts(true), // Use silent refresh
          loadContactRequests(true) // Use silent refresh
        ]);
      } catch (refreshError) {
        console.warn('Error refreshing data after accepting contact', refreshError);
        // Continue since the main operation succeeded
      }

      setError(null);
      return { success: true };
    } catch (err) {
      console.error('Failed to accept contact request:', err);

      // Create a more detailed error message
      const errorDetails = err.response?.data?.detail || 'Failed to accept contact request';
      const statusCode = err.response?.status || 'unknown';
      const errorMessage = `Failed to accept request (${statusCode}): ${errorDetails}`;

      setError(errorMessage);

      return {
        success: false,
        message: errorMessage,
        error: err
      };
    } finally {
      setRequestsLoading(false);
    }
  };

  const rejectContactRequest = async (requestId) => {
    setRequestsLoading(true);
    try {
      console.log(`Rejecting contact request with ID: ${requestId}`);

      // Try both endpoint formats
      try {
        await api.post(`/contacts/reject/${requestId}`);
      } catch (firstAttemptError) {
        console.log('First attempt failed, trying alternative endpoint format');
        await api.post(`/contact/deny/${requestId}`);
      }

      console.log('Contact request rejected successfully');

      // Refresh contact requests after rejecting
      try {
        await loadContactRequests(true); // Use silent refresh
      } catch (refreshError) {
        console.warn('Error refreshing data after rejecting contact', refreshError);
      }

      setError(null);
      return { success: true };
    } catch (err) {
      console.error('Failed to reject contact request:', err);

      const errorDetails = err.response?.data?.detail || 'Failed to reject contact request';
      const statusCode = err.response?.status || 'unknown';
      const errorMessage = `Failed to reject request (${statusCode}): ${errorDetails}`;

      setError(errorMessage);

      return {
        success: false,
        message: errorMessage,
        error: err
      };
    } finally {
      setRequestsLoading(false);
    }
  };

  const removeContact = async (userId) => {
    setContactsLoading(true);
    try {
      await api.delete(`/contacts/${userId}`);
      await loadContacts();
      setError(null);
    } catch (err) {
      console.error('Failed to remove contact:', err);
      setError('Failed to remove contact. Please try again.');
      throw err;
    } finally {
      setContactsLoading(false);
    }
  };

  const value = {
    contacts,
    contactRequests,
    sentRequests,
    loading: {
      contacts: contactsLoading,
      requests: requestsLoading,
      sentRequests: sentRequestsLoading,
      search: searchLoading,
      any: contactsLoading || requestsLoading || sentRequestsLoading
    },
    error,
    searchResults,
    searchLoading,
    searchUsers,
    sendContactRequest,
    acceptContactRequest,
    rejectContactRequest,
    removeContact,
    refreshContacts: loadContacts,
    refreshRequests: loadContactRequests,
    refreshSentRequests: loadSentRequests
  };

  return (
    <ContactsContext.Provider value={value}>
      {children}
    </ContactsContext.Provider>
  );
}