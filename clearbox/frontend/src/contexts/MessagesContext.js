import React, { createContext, useState, useContext, useEffect } from 'react';
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
  
  // Add a ref to track if messages are loaded for a given chat
  const loadedChatsRef = React.useRef(new Set());
  
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
      
      // Process messages to protect content from being encrypted
      const processedMessages = response.data.map(msg => {
        // First check existing messages in state
        const existingMsg = messages[userId]?.find(m => m.id === msg.id);
        
        // Then check localStorage for preserved content
        const preservedContent = getPreservedContent(msg.id, null);
        
        // Use the best available content prioritizing existing message content
        const content = (existingMsg?.content && existingMsg.content !== "Message content could not be displayed") 
          ? existingMsg.content
          : preservedContent
            ? preservedContent
            : (msg.content !== "[Encrypted message]")
              ? msg.content
              : "Message content could not be displayed";
        
        return {
          ...msg,
          content,
          decrypted: true,
          preserve_content: true
        };
      });
      
      // Store messages indexed by user ID, but preserve existing messages
      setMessages(prev => {
        const existingMessages = prev[userId] || [];
        
        // If we already have messages, merge them with the new ones
        if (existingMessages.length > 0) {
          const existingIds = new Set(existingMessages.map(msg => msg.id));
          
          // Add new messages that don't exist yet
          const newMessages = processedMessages.filter(msg => !existingIds.has(msg.id));
          
          // Update existing messages, keeping original content
          const updatedExistingMessages = existingMessages.map(existingMsg => {
            const updatedMsg = processedMessages.find(m => m.id === existingMsg.id);
            if (updatedMsg && existingMsg.content && existingMsg.content !== "Message content could not be displayed") {
              return {
                ...updatedMsg,
                content: existingMsg.content,
                preserve_content: true
              };
            }
            return existingMsg;
          });
          
          return {
            ...prev,
            [userId]: [...updatedExistingMessages, ...newMessages]
          };
        }
        
        // If no existing messages, use the processed ones
        return {
          ...prev,
          [userId]: processedMessages
        };
      });
      
      // Track that we've loaded messages for this chat
      loadedChatsRef.current.add(userId);
      setError(null);
    } catch (error) {
      console.error(`Error loading messages for user ${userId}:`, error);
      setError(`Failed to load messages. ${error.message || 'Please try again'}`);
    } finally {
      if (!silent && isInitialLoad) {
        setLoading(false);
      }
    }
  };

  // Replace the one-time load with auto-refresh
  useEffect(() => {
    if (activeChat) {
      // Load messages initially
      loadMessages(activeChat);
      
      // Set up a polling interval to check for new messages
      const intervalId = setInterval(() => {
        // Use a separate function for polling to avoid conflicting with the main load
        pollForNewMessages(activeChat);
      }, 3000); // Check every 3 seconds
      
      // Clean up the interval when component unmounts or activeChat changes
      return () => clearInterval(intervalId);
    }
  }, [activeChat]);

  // Update the polling function to handle errors better and use the correct endpoints
  const pollForNewMessages = async (userId) => {
    if (!userId || !currentUser) return;
    
    try {
      // Instead of using the /since endpoint which seems to not exist,
      // just fetch all messages and filter client-side
      const response = await api.get(`/messages/user/${userId}`);
      
      // Ensure we have a valid array response
      if (!response.data || !Array.isArray(response.data)) {
        console.warn('Received invalid messages data format in polling:', response.data);
        return;
      }
      
      // Filter for new messages client-side based on what we already have
      const existingMessages = messages[userId] || [];
      const existingIds = new Set(existingMessages.map(msg => msg.id));
      
      // Find messages in the response that aren't in our existing messages
      const newMessages = response.data
        .filter(msg => !existingIds.has(msg.id))
        .map(msg => ({
          ...msg,
          content: msg.content,
          decrypted: true,
          preserve_content: true
        }));
      
      // If no new messages, do nothing
      if (newMessages.length === 0) {
        return;
      }
      
      // Update our messages state with the new messages
      setMessages(prev => {
        const currentMessages = prev[userId] || [];
        return {
          ...prev,
          [userId]: [...currentMessages, ...newMessages]
        };
      });
    } catch (error) {
      console.error("Error polling for new messages:", error);
      // Don't set error state to avoid UI disruption, just log it
    }
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

  // Update the sendMessage function to use the correct endpoint
  const sendMessage = async (recipientId, content) => {
    if (!recipientId || !content || !currentUser) {
      throw new Error('Missing required data to send message');
    }
    
    try {
      const payload = {
        recipient_id: recipientId,
        content: content
      };
      
      // Add optimistic update for immediate UI feedback
      const tempId = `temp-${Date.now()}`;
      const optimisticMessage = {
        id: tempId,
        content,
        sender_id: currentUser.id,
        from_user: currentUser.id,
        to_user: recipientId,
        chat_id: recipientId,
        timestamp: new Date().toISOString(),
        created_at: new Date().toISOString(),
        read: false,
        decrypted: true,
        preserve_content: true,
        pending: true
      };
      
      // Add the optimistic message to state
      setMessages(prev => {
        const existingMessages = prev[recipientId] || [];
        return {
          ...prev,
          [recipientId]: [...existingMessages, optimisticMessage]
        };
      });
      
      // Try multiple endpoints in case one fails
      let response;
      try {
        // Try the most likely endpoint first
        response = await api.post('/messages', payload);
      } catch (firstError) {
        console.log('First endpoint failed, trying alternative endpoint', firstError);
        try {
          // Try alternative endpoint format
          response = await api.post('/messages/send', payload);
        } catch (secondError) {
          console.log('Second endpoint failed, trying final endpoint', secondError);
          // Try one more format as last resort
          response = await api.post(`/messages/user/${recipientId}`, payload);
        }
      }
      
      // Update the message with the real ID and remove pending status
      if (response && response.data && response.data.id) {
        setMessages(prev => {
          const updatedMessages = (prev[recipientId] || []).map(msg => 
            msg.id === tempId ? { ...msg, id: response.data.id, pending: false } : msg
          );
          
          return {
            ...prev,
            [recipientId]: updatedMessages
          };
        });
        
        // Save message content to localStorage for content preservation
        try {
          const savedMessages = JSON.parse(localStorage.getItem('preservedMessages') || '{}');
          savedMessages[response.data.id] = { id: response.data.id, content };
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
        
        return {
          ...prev,
          [recipientId]: updatedMessages
        };
      });
      
      throw error;
    }
  };

  const markAsRead = async (messageId) => {
    try {
      await api.post(`/messages/read/${messageId}`);
    } catch (err) {
      console.error('Failed to mark message as read:', err);
    }
  };

  // Add helper to check localStorage for preserved content
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
    loadMessages,
    refreshMessages,
    markAsRead,
    getPreservedContent
  };

  return (
    <MessagesContext.Provider value={value}>
      {children}
    </MessagesContext.Provider>
  );
} 