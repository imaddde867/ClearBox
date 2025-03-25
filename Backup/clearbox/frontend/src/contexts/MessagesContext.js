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
      
      // Mark this chat as loaded regardless of message count
      loadedChatsRef.current.add(userId);
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

  // Function to poll for new messages without full reloading
  const pollForNewMessages = async (userId) => {
    if (!userId) return;
    
    // Check for authentication token first
    const token = localStorage.getItem('clearboxToken');
    if (!token) {
      console.warn('Cannot poll for messages: No authentication token available');
      return;
    }
    
    try {
      const response = await api.get(`/messages/user/${userId}`);
      
      // Process received messages to ALWAYS preserve original content
      const processedMessages = response.data.map(msg => {
        // First check localStorage for preserved content
        const preservedContent = getPreservedContent(msg.id, null);
        
        // Then check existing messages in state - IMPORTANT: don't check if it's "[Encrypted message]"
        const existingMsg = messages[userId]?.find(m => m.id === msg.id);
        
        // Use the best available content (preserved > existing > original) without checking if encrypted
        // This ensures we never replace good content with the fallback
        const content = preservedContent || 
                        (existingMsg?.content && existingMsg.content !== "Message content could not be displayed" ? existingMsg.content : null) || 
                        (msg.content !== "[Encrypted message]" ? msg.content : "Message content could not be displayed");
          
        return {
          ...msg,
          content: content,
          decrypted: true,
          preserve_content: true
        };
      });

      // Compare with existing messages and update state correctly
      setMessages(prev => {
        const existingMessages = prev[userId] || [];
        const existingIds = new Set(existingMessages.map(msg => msg.id));
        
        // Find messages that don't exist in our current state
        const newMessages = processedMessages.filter(msg => !existingIds.has(msg.id));
        
        // Update existing messages to preserve content - NEVER overwrite good content
        const updatedExistingMessages = existingMessages.map(existingMsg => {
          const updatedMsg = processedMessages.find(m => m.id === existingMsg.id);
          
          // If we have an existing message with real content, always keep it
          if (updatedMsg && existingMsg.content && existingMsg.content !== "Message content could not be displayed") {
            return {
              ...updatedMsg,
              content: existingMsg.content, // Always keep the original content
              preserve_content: true
            };
          }
          
          // Otherwise return existing message unchanged
          return existingMsg;
        });
        
        // If no new messages, don't update state at all
        if (newMessages.length === 0) {
          return prev;
        }
        
        // Otherwise, update with new messages
        return {
          ...prev,
          [userId]: [...updatedExistingMessages, ...newMessages]
        };
      });
    } catch (err) {
      console.error('Error polling for new messages:', err.response?.status, err.response?.data);
      
      // Handle authentication errors specifically
      if (err.response?.status === 401) {
        console.error('Authentication error during message polling. Token may be invalid.');
        // Don't emit an auth error event here to avoid interrupting the user,
        // but stop polling silently
        return;
      }
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

  // Modify sendMessage to save messages to localStorage and handle auth errors
  const sendMessage = async (recipientId, content) => {
    if (!recipientId || !content || !content.trim()) return;
    
    // Check for authentication token first
    const token = localStorage.getItem('clearboxToken');
    if (!token) {
      console.error('Cannot send message: No authentication token available');
      throw new Error('Authentication required. Please log in again.');
    }
    
    // Generate a unique temp ID that won't collide with actual message IDs
    const tempId = `temp-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    // Store the actual message content for preservation
    const actualContent = content.trim();
    
    try {
      // Create a message object for immediate display with final content
      const optimisticMessage = {
        id: tempId,
        sender_id: currentUser.id,
        receiver_id: recipientId,
        content: actualContent, // Use actual content
        created_at: new Date().toISOString(),
        timestamp: new Date().toISOString(),
        delivered: true,
        preserve_content: true // Flag to prevent content changes
      };
      
      // Add message to UI immediately (optimistic update)
      setMessages(prevMessages => {
        const existingMessages = prevMessages[recipientId] || [];
        return {
          ...prevMessages,
          [recipientId]: [...existingMessages, optimisticMessage]
        };
      });
      
      // Send to backend
      const messageData = {
        receiver_id: recipientId,
        content: actualContent
      };
      
      // Use setTimeout to artificially delay the API call to ensure UI updates first
      await new Promise(resolve => setTimeout(resolve, 10));
      
      console.log('Sending message to backend:', messageData);
      const response = await api.post('/messages', messageData);
      console.log('Message sent successfully:', response.data);
      
      // Update with server response (replace temp message with real one)
      const newMessage = {
        id: response.data.id || tempId, // Fallback to temp ID if server doesn't return one
        sender_id: currentUser.id,
        receiver_id: recipientId,
        content: actualContent, // Keep using the original content, ignore any server changes
        created_at: response.data.created_at || new Date().toISOString(),
        timestamp: response.data.timestamp || new Date().toISOString(),
        delivered: true,
        preserve_content: true // Flag to prevent content changes
      };
      
      // Replace the temporary message with the confirmed one
      setMessages(prevMessages => {
        const existingMessages = prevMessages[recipientId] || [];
        const updatedMessages = existingMessages.map(msg => 
          msg.id === tempId ? newMessage : msg
        );
        
        return {
          ...prevMessages,
          [recipientId]: updatedMessages
        };
      });
      
      // After successfully sending the message, save it to localStorage
      try {
        const savedMessages = JSON.parse(localStorage.getItem('preservedMessages') || '{}');
        savedMessages[newMessage.id] = {
          id: newMessage.id,
          content: actualContent
        };
        localStorage.setItem('preservedMessages', JSON.stringify(savedMessages));
      } catch (e) {
        console.error('Error saving message to localStorage', e);
      }
      
      return response.data;
    } catch (err) {
      console.error('Error sending message:', err.response?.status, err.response?.data);
      
      // Handle authentication errors specifically
      if (err.response?.status === 401) {
        console.error('Authentication error while sending message. Token may be invalid.');
        
        // Emit an auth error event to notify the auth context
        const authErrorEvent = new CustomEvent('auth:error', { 
          detail: { message: 'Session expired while sending message. Please log in again.' }
        });
        window.dispatchEvent(authErrorEvent);
      }
      
      // Keep the message visible but mark it as failed
      setMessages(prevMessages => {
        const existingMessages = prevMessages[recipientId] || [];
        const updatedMessages = existingMessages.map(msg => 
          msg.id === tempId ? { 
            ...msg, 
            failed: true,
            error: err.response?.data?.detail || 'Failed to send',
            content: actualContent, // Ensure content is preserved even if failed
            preserve_content: true
          } : msg
        );
        
        return {
          ...prevMessages,
          [recipientId]: updatedMessages
        };
      });
      
      throw new Error(err.response?.data?.detail || 'Failed to send message');
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