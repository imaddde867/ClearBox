import React, { createContext, useState, useContext, useEffect, useRef } from 'react';
import api from '../services/api';
import { useAuth } from './AuthContext';

const MessagesContext = createContext();

export function useMessages() {
  return useContext(MessagesContext);
}

export function MessagesProvider({ children }) {
  const { currentUser } = useAuth();
  const [messages, setMessages] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeChat, setActiveChat] = useState(null);
  const [websocket, setWebsocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  // Add a ref to track if messages are loaded for a given chat
  const loadedChatsRef = useRef(new Set());

  // Fetch messages for the active chat
  const loadMessages = async (userId, silent = false) => {
    if (!userId) return;

    const isInitialLoad = !loadedChatsRef.current.has(userId);

    try {
      // Only show loading indicator on initial load
      if (!silent && isInitialLoad) {
        setLoading(true);
      }

      // First attempt - get messages from state if they exist
      if (messages[userId] && messages[userId].length > 0) {
        // Even if we have messages, we should still refresh them
        // But we won't show loading indicator for better UX
        if (!silent && isInitialLoad) {
          setLoading(false);
        }
      }

      const response = await api.get(`/messages/user/${userId}`);

      if (!response.data || !Array.isArray(response.data)) {
        console.warn('Received invalid messages data format:', response.data);
        // Initialize as empty array if not valid
        response.data = [];
      }

      // Process messages - we need to restore any preserved message content
      const processedMessages = response.data.map(msg => {
        // Check localStorage for preserved content
        const preservedContent = getPreservedContent(msg.id, null);

        // If we have preserved content, use it instead of what the server sent
        if (preservedContent) {
          return {
            ...msg,
            content: preservedContent,
            decrypted: true,
            preserve_content: true
          };
        }

        return {
          ...msg,
          decrypted: true
        };
      });

      // Sort messages by timestamp to ensure correct order
      processedMessages.sort((a, b) => {
        const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
        const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
        return timeA - timeB;
      });

      // Update state with messages
      setMessages(prev => ({
        ...prev,
        [userId]: processedMessages
      }));

      // Mark as loaded
      loadedChatsRef.current.add(userId);

      // Clear error state
      setError(null);
    } catch (err) {
      console.error('Error loading messages:', err);
      // Don't set error state to avoid UI flickering

      // Still keep any messages we have
      if (!messages[userId]) {
        setMessages(prev => ({
          ...prev,
          [userId]: [] // Empty array to avoid continuous loading attempts
        }));

        // Even if there's an error, mark as loaded to prevent infinite loading
        loadedChatsRef.current.add(userId);
      }
    } finally {
      // Always turn off loading regardless of success/failure
      setLoading(false);
    }
  };

  // Set up WebSocket connection when user logs in
  useEffect(() => {
    if (!currentUser || !currentUser.id) return;

    // Get token from localStorage
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No authentication token available for WebSocket connection');
      return;
    }

    // Connect to WebSocket
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const socket = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${token}`);

    socket.onopen = () => {
      console.log('WebSocket connection established');
      setIsConnected(true);
      setWebsocket(socket);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
      setIsConnected(false);
      setWebsocket(null);

      // Try to reconnect after a delay
      setTimeout(() => {
        console.log('Attempting to reconnect WebSocket...');
        // The effect will run again, creating a new connection
      }, 5000);
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Received WebSocket message:', data);

        // Dispatch event to the window so App.js can also process it
        const customEvent = new CustomEvent('ws-message', { detail: data });
        window.dispatchEvent(customEvent);

        // Handle different message types
        if (data.type === 'message') {
          // Direct message received
          handleIncomingMessage(data);
        } else if (data.type === 'group_message') {
          // Group message received
          handleIncomingGroupMessage(data);
        } else if (data.type === 'presence') {
          // Presence update (online/offline status)
          console.log(`User ${data.userId} is ${data.online ? 'online' : 'offline'}`);
          // We don't handle this here as it's managed in App.js
        }
      } catch (error) {
        console.error('Error processing WebSocket message:', error);
      }
    };

    // Set up ping interval to keep connection alive
    const pingInterval = setInterval(() => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000); // every 30 seconds

    // Clean up on unmount or user change
    return () => {
      clearInterval(pingInterval);
      if (socket) {
        socket.close();
      }
    };
  }, [currentUser]);

  // Handle incoming direct message
  const handleIncomingMessage = (data) => {
    const { messageId, senderId, content, timestamp } = data;

    // Add to state
    setMessages(prev => {
      // Process both the sender's chat and the active chat
      const chatId = senderId;
      const existingMessages = prev[chatId] || [];

      // Check if we already have this message (avoid duplicates)
      if (existingMessages.some(msg => msg.id === messageId)) {
        return prev;
      }

      // Create new message object with a properly parsed timestamp
      const parsedTimestamp = new Date(timestamp).toISOString();
      const newMessage = {
        id: messageId,
        sender_id: senderId,
        receiver_id: currentUser.id,
        content: content,
        created_at: parsedTimestamp,
        timestamp: parsedTimestamp, // Ensure we have both timestamp formats
        decrypted: true,
        delivered: true
      };

      // Save content to localStorage for preservation
      try {
        const savedMessages = JSON.parse(localStorage.getItem('preservedMessages') || '{}');
        savedMessages[messageId] = { id: messageId, content };
        localStorage.setItem('preservedMessages', JSON.stringify(savedMessages));
      } catch (e) {
        console.error('Error saving message to localStorage', e);
      }

      // Create new messages array with proper sorting
      const updatedMessages = [...existingMessages, newMessage];

      // Sort all messages by timestamp in ascending order (oldest first)
      updatedMessages.sort((a, b) => {
        // Ensure we have standard date objects for comparison
        const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
        const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
        return timeA - timeB;
      });

      // Create new state with updated messages
      const newState = { ...prev };

      // Update the sender's chat in the state
      newState[chatId] = updatedMessages;

      return newState;
    });

    // Acknowledge receipt
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({
        type: 'read_message',
        messageId
      }));
    }
  };

  // Handle incoming group message
  const handleIncomingGroupMessage = (data) => {
    const { messageId, senderId, groupId, content, timestamp } = data;

    // Add to state - store messages by groupId with "group-" prefix to distinguish from user chats
    setMessages(prev => {
      const chatKey = `group-${groupId}`;
      const existingMessages = prev[chatKey] || [];

      // Check if we already have this message (avoid duplicates)
      const isDuplicate = existingMessages.some(msg => 
        msg.id === messageId || 
        (msg.content === content && 
         msg.sender_id === senderId &&
         new Date(msg.timestamp || msg.created_at).getTime() === new Date(timestamp).getTime())
      );

      if (isDuplicate) {
        return prev;
      }

      // Add the new message
      const newMessage = {
        id: messageId,
        content,
        sender_id: senderId,
        group_id: groupId,
        timestamp,
        created_at: timestamp,
        delivered: true,
        decrypted: true
      };

      // Create a new array with the message added
      const updatedMessages = [...existingMessages, newMessage];

      // Sort messages by timestamp
      updatedMessages.sort((a, b) => {
        const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
        const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
        return timeA - timeB;
      });

      // Return updated state
      return {
        ...prev,
        [chatKey]: updatedMessages
      };
    });
  };

  // Add a public refresh function that follows the same pattern as in ContactsContext
  const refreshMessages = async (userId, silent = false) => {
    if (!userId) return;

    console.log(`Refreshing messages for user ${userId}...`);
    await loadMessages(userId, silent);
    return true;
  };

  // Add useEffect to load preserved messages from localStorage
  useEffect(() => {
    // Load any preserved messages from localStorage
    try {
      const savedMessages = JSON.parse(localStorage.getItem('preservedMessages') || '{}');
      if (Object.keys(savedMessages).length > 0) {
        console.log('Loaded preserved messages from localStorage:', Object.keys(savedMessages).length);
      }
    } catch (e) {
      console.error('Error loading preserved messages from localStorage', e);
    }
  }, []);

  // Use the activeChat to load messages when it changes
  useEffect(() => {
    if (activeChat) {
      loadMessages(activeChat);
    }
  }, [activeChat]);

  // Send message function
  const sendMessage = async (recipientId, content) => {
    if (!recipientId || !content || !content.trim() || !currentUser) {
      throw new Error('Missing required data to send message');
    }

    try {
      const payload = {
        receiver_id: recipientId,
        content: content.trim()
      };

      // Create a consistent timestamp for the optimistic message
      const now = new Date();
      const isoTimestamp = now.toISOString();

      // Add optimistic update for immediate UI feedback
      const tempId = `temp-${Date.now()}`;
      const optimisticMessage = {
        id: tempId,
        content: content.trim(),
        sender_id: currentUser.id,
        receiver_id: recipientId,
        timestamp: isoTimestamp,
        created_at: isoTimestamp,
        delivered: false,
        decrypted: true,
        preserve_content: true,
        pending: true
      };

      // Add the optimistic message to state
      setMessages(prev => {
        const existingMessages = prev[recipientId] || [];

        // Add new message to existing ones
        const updatedMessages = [...existingMessages, optimisticMessage];

        // Sort messages by timestamp in ascending order (oldest first)
        updatedMessages.sort((a, b) => {
          // Ensure we have standard date objects for comparison
          const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
          const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
          return timeA - timeB;
        });

        return {
          ...prev,
          [recipientId]: updatedMessages
        };
      });

      // Send message to server
      const response = await api.post('/messages', payload);

      // Update the message with the real ID and remove pending status
      if (response && response.data && response.data.id) {
        setMessages(prev => {
          const updatedMessages = (prev[recipientId] || []).map(msg =>
            msg.id === tempId ? {
              ...msg,
              id: response.data.id,
              timestamp: response.data.created_at || msg.timestamp, // Use server timestamp if available
              created_at: response.data.created_at || msg.created_at,
              pending: false
            } : msg
          );

          // Ensure messages are sorted by timestamp
          updatedMessages.sort((a, b) => {
            // Ensure we have standard date objects for comparison
            const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
            const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
            return timeA - timeB;
          });

          return {
            ...prev,
            [recipientId]: updatedMessages
          };
        });

        // Save message content to localStorage for content preservation
        try {
          const savedMessages = JSON.parse(localStorage.getItem('preservedMessages') || '{}');
          savedMessages[response.data.id] = { id: response.data.id, content: content.trim() };
          localStorage.setItem('preservedMessages', JSON.stringify(savedMessages));
        } catch (e) {
          console.error('Error saving message to localStorage', e);
        }
      }

      return response?.data;
    } catch (error) {
      console.error('Error sending message:', error);

      // Update the optimistic message to show error state
      setMessages(prev => {
        const updatedMessages = (prev[recipientId] || []).map(msg =>
          msg.pending ? {
            ...msg,
            error: true,
            errorMessage: error?.response?.data?.detail || 'Failed to send'
          } : msg
        );

        // Ensure messages are sorted by timestamp
        updatedMessages.sort((a, b) => {
          // Ensure we have standard date objects for comparison
          const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
          const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
          return timeA - timeB;
        });

        return {
          ...prev,
          [recipientId]: updatedMessages
        };
      });

      throw error;
    }
  };

  // Add a function to send group messages
  const sendGroupMessage = async (groupId, content) => {
    if (!groupId || !content || !content.trim() || !currentUser) {
      throw new Error('Missing required data to send group message');
    }

    try {
      const payload = {
        group_id: groupId,
        content: content.trim()
      };

      // Create a consistent timestamp for the optimistic message
      const now = new Date();
      const isoTimestamp = now.toISOString();

      // Add optimistic update for immediate UI feedback
      const tempId = `temp-${Date.now()}`;
      const optimisticMessage = {
        id: tempId,
        content: content.trim(),
        sender_id: currentUser.id,
        group_id: groupId,
        timestamp: isoTimestamp,
        created_at: isoTimestamp,
        delivered: true,
        decrypted: true,
        preserve_content: true,
        pending: true
      };

      // Add the optimistic message to state with group- prefix
      const chatKey = `group-${groupId}`;
      setMessages(prev => {
        const existingMessages = prev[chatKey] || [];

        // Add new message to existing ones
        const updatedMessages = [...existingMessages, optimisticMessage];

        // Sort messages by timestamp in ascending order (oldest first)
        updatedMessages.sort((a, b) => {
          const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
          const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
          return timeA - timeB;
        });

        return {
          ...prev,
          [chatKey]: updatedMessages
        };
      });

      // Send message to server
      const response = await api.post('/messages', payload);

      // Update the message with the real ID and remove pending status
      if (response && response.data && response.data.id) {
        setMessages(prev => {
          const chatKey = `group-${groupId}`;
          const updatedMessages = (prev[chatKey] || []).map(msg =>
            msg.id === tempId ? {
              ...msg,
              id: response.data.id,
              timestamp: response.data.created_at || msg.timestamp,
              created_at: response.data.created_at || msg.created_at,
              pending: false
            } : msg
          );

          // Ensure messages are sorted by timestamp
          updatedMessages.sort((a, b) => {
            const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
            const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
            return timeA - timeB;
          });

          return {
            ...prev,
            [chatKey]: updatedMessages
          };
        });

        // Save message content to localStorage for content preservation
        try {
          const savedMessages = JSON.parse(localStorage.getItem('preservedMessages') || '{}');
          savedMessages[response.data.id] = { id: response.data.id, content: content.trim() };
          localStorage.setItem('preservedMessages', JSON.stringify(savedMessages));
        } catch (e) {
          console.error('Error saving message to localStorage', e);
        }
      }

      return response?.data;
    } catch (error) {
      console.error('Error sending group message:', error);

      // Update the optimistic message to show error state
      const chatKey = `group-${groupId}`;
      setMessages(prev => {
        const updatedMessages = (prev[chatKey] || []).map(msg =>
          msg.pending ? {
            ...msg,
            error: true,
            errorMessage: error?.response?.data?.detail || 'Failed to send'
          } : msg
        );

        return {
          ...prev,
          [chatKey]: updatedMessages
        };
      });

      throw error;
    }
  };

  // Function to load group messages
  const loadGroupMessages = async (groupId, silent = false) => {
    if (!groupId) return;

    const chatKey = `group-${groupId}`;
    const isInitialLoad = !loadedChatsRef.current.has(chatKey);

    try {
      // Only show loading indicator on initial load
      if (!silent && isInitialLoad) {
        setLoading(true);
      }

      const response = await api.get(`/messages/group/${groupId}`);

      if (!response.data || !Array.isArray(response.data)) {
        console.warn('Received invalid group messages data format:', response.data);
        // Initialize as empty array if not valid
        response.data = [];
      }

      // Process messages and restore preserved content
      const processedMessages = response.data.map(msg => {
        const preservedContent = getPreservedContent(msg.id, null);

        if (preservedContent) {
          return {
            ...msg,
            content: preservedContent,
            decrypted: true,
            preserve_content: true
          };
        }

        return {
          ...msg,
          decrypted: true
        };
      });

      // Sort messages by timestamp
      processedMessages.sort((a, b) => {
        const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
        const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
        return timeA - timeB;
      });

      // Update state with messages
      setMessages(prev => ({
        ...prev,
        [chatKey]: processedMessages
      }));

      // Mark as loaded
      loadedChatsRef.current.add(chatKey);

      // Clear error state
      setError(null);
    } catch (err) {
      console.error('Error loading group messages:', err);

      // Still keep any messages we have
      if (!messages[chatKey]) {
        setMessages(prev => ({
          ...prev,
          [chatKey]: [] // Empty array to avoid continuous loading attempts
        }));

        // Even if there's an error, mark as loaded to prevent infinite loading
        loadedChatsRef.current.add(chatKey);
      }
    } finally {
      // Always turn off loading regardless of success/failure
      setLoading(false);
    }
  };

  // Add a public refresh function for group messages
  const refreshGroupMessages = async (groupId, silent = false) => {
    if (!groupId) return;

    console.log(`Refreshing messages for group ${groupId}...`);
    await loadGroupMessages(groupId, silent);
    return true;
  };

  const markAsRead = async (messageId) => {
    try {
      await api.put(`/messages/${messageId}/delivered`);
    } catch (err) {
      console.error('Failed to mark message as read:', err);
    }
  };

  // Helper to check localStorage for preserved content
  const getPreservedContent = (messageId, defaultContent) => {
    try {
      const savedMessages = JSON.parse(localStorage.getItem('preservedMessages') || '{}');
      return savedMessages[messageId]?.content || defaultContent;
    } catch (e) {
      return defaultContent;
    }
  };

  const value = {
    messages,
    loading,
    error,
    activeChat,
    setActiveChat,
    sendMessage,
    sendGroupMessage,
    loadMessages,
    loadGroupMessages,
    refreshMessages,
    refreshGroupMessages,
    markAsRead,
    getPreservedContent,
    isConnected
  };

  return (
    <MessagesContext.Provider value={value}>
      {children}
    </MessagesContext.Provider>
  );
}