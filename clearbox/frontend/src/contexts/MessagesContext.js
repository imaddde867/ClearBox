import React, { createContext, useState, useContext, useEffect, useRef } from 'react';
import api from '../services/api';
import { useAuth } from './AuthContext';
import mqttService from '../services/mqtt';
import { MQTT_CONFIG } from '../config';

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
  const [mqttConnected, setMqttConnected] = useState(false);

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

  // Set up MQTT connection when user logs in
  useEffect(() => {
    if (!currentUser || !currentUser.id) return;

    // Get token from localStorage
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No authentication token available for MQTT connection');
      return;
    }

    console.log('Setting up MQTT connection for user:', currentUser.id);

    // Initialize MQTT connection
    mqttService.initializeMQTT(currentUser.id, token)
      .then(() => {
        console.log('MQTT connection initialized successfully');
      })
      .catch(error => {
        console.error('Failed to initialize MQTT connection:', error);
      });

    // Subscribe to connection status changes
    const unsubscribeStatus = mqttService.onConnectionStatus(isConnected => {
      console.log('MQTT connection status changed:', isConnected);
      setMqttConnected(isConnected);
    });

    // Subscribe to message events
    const unsubscribeMessages = mqttService.onMessage((topic, data) => {
      console.log(`Message received on topic ${topic}:`, data);
      
      // Handle user messages
      if (topic.startsWith('user/') && topic.endsWith('/messages')) {
        handleIncomingMessage(data);
      }
      // Handle group messages
      else if (topic.startsWith('group/') && topic.endsWith('/messages')) {
        handleIncomingGroupMessage(data);
      }
    });

    // Subscribe to additional topics as needed
    if (activeChat) {
      // Subscribe to active chat topic
      const chatTopic = activeChat.isGroup 
        ? MQTT_CONFIG.TOPICS.GROUP_MESSAGES(activeChat.id)
        : MQTT_CONFIG.TOPICS.USER_MESSAGES(activeChat.id);
      
      mqttService.subscribeTopic(chatTopic)
        .catch(error => {
          console.error(`Failed to subscribe to ${chatTopic}:`, error);
        });
    }

    // Set up ping interval to keep connection alive
    const pingInterval = setInterval(() => {
      if (mqttService.isConnected()) {
        // Send a ping message to keep the connection alive
        mqttService.publishMessage('ping', JSON.stringify({ 
          type: 'ping', 
          userId: currentUser.id,
          timestamp: new Date().toISOString()
        })).catch(error => {
          console.error('Failed to send ping:', error);
        });
      }
    }, 30000); // every 30 seconds

    // Clean up on unmount or user change
    return () => {
      clearInterval(pingInterval);
      unsubscribeStatus();
      unsubscribeMessages();
      mqttService.disconnectMQTT();
    };
  }, [currentUser]);

  // Subscribe to active chat topic when activeChat changes
  useEffect(() => {
    if (!currentUser || !activeChat || !mqttConnected) return;

    // Determine topic based on chat type
    const chatTopic = activeChat.isGroup 
      ? MQTT_CONFIG.TOPICS.GROUP_MESSAGES(activeChat.id)
      : MQTT_CONFIG.TOPICS.USER_MESSAGES(activeChat.id);
    
    console.log(`Subscribing to active chat topic: ${chatTopic}`);
    
    mqttService.subscribeTopic(chatTopic)
      .catch(error => {
        console.error(`Failed to subscribe to ${chatTopic}:`, error);
      });

    return () => {
      // Unsubscribe from topic when component unmounts or activeChat changes
      mqttService.unsubscribeTopic(chatTopic)
        .catch(error => {
          console.error(`Failed to unsubscribe from ${chatTopic}:`, error);
        });
    };
  }, [currentUser, activeChat, mqttConnected]);

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

  // Modify sendMessage to use MQTT instead of WebSocket when possible
  const sendMessage = async (recipientId, content) => {
    if (!currentUser || !content.trim()) {
      console.error('Cannot send message: no user or empty content');
      return null;
    }

    // Generate a temporary ID for the message
    const tempMessageId = `temp_${new Date().getTime()}_${Math.random().toString(36).substring(2, 9)}`;
    const timestamp = new Date().toISOString();

    // Create a new message object
    const newMessage = {
      id: tempMessageId,
      sender_id: currentUser.id,
      receiver_id: recipientId,
      content: content,
      timestamp: timestamp,
      status: 'sending',
      is_read: false,
      // Add any other properties your message objects have
    };

    // Optimistically add to state
    setMessages(prev => {
      const existingMessages = prev[recipientId] || [];
      return {
        ...prev,
        [recipientId]: [...existingMessages, newMessage]
      };
    });

    try {
      // Attempt to send via MQTT if connected
      if (mqttConnected) {
        // Publish to the recipient's topic
        const recipientTopic = MQTT_CONFIG.TOPICS.USER_MESSAGES(recipientId);
        
        // Create the message payload
        const payload = {
          type: 'message',
          messageId: tempMessageId,
          senderId: currentUser.id,
          recipientId: recipientId,
          content: content,
          timestamp: timestamp
        };
        
        // Send via MQTT
        await mqttService.publishMessage(recipientTopic, payload);
        
        // Update status to 'sent' in local state
        setMessages(prev => {
          const chatMessages = prev[recipientId] || [];
          return {
            ...prev,
            [recipientId]: chatMessages.map(msg => 
              msg.id === tempMessageId 
                ? { ...msg, status: 'sent', timestamp: timestamp }
                : msg
            )
          };
        });
        
        console.log('Message sent via MQTT');
      } else {
        // Fall back to REST API
        const response = await api.post(`/messages/user/${recipientId}`, {
          content: content
        });
        
        // Update the message in state with the server response
        if (response.data && response.data.id) {
          setMessages(prev => {
            const chatMessages = prev[recipientId] || [];
            return {
              ...prev,
              [recipientId]: chatMessages.map(msg => 
                msg.id === tempMessageId 
                  ? { ...msg, id: response.data.id, status: 'sent', timestamp: response.data.timestamp || timestamp }
                  : msg
              )
            };
          });
        }
        
        console.log('Message sent via REST API');
      }
      
      return true;
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Update status to 'failed' in local state
      setMessages(prev => {
        const chatMessages = prev[recipientId] || [];
        return {
          ...prev,
          [recipientId]: chatMessages.map(msg => 
            msg.id === tempMessageId 
              ? { ...msg, status: 'failed' }
              : msg
          )
        };
      });
      
      return false;
    }
  };

  // Similarly modify sendGroupMessage to use MQTT
  const sendGroupMessage = async (groupId, content) => {
    if (!currentUser || !content.trim()) {
      console.error('Cannot send group message: no user or empty content');
      return null;
    }

    // Generate a temporary ID for the message
    const tempMessageId = `temp_${new Date().getTime()}_${Math.random().toString(36).substring(2, 9)}`;
    const timestamp = new Date().toISOString();
    const chatKey = `group-${groupId}`;

    // Create a new message object
    const newMessage = {
      id: tempMessageId,
      sender_id: currentUser.id,
      group_id: groupId,
      content: content,
      timestamp: timestamp,
      status: 'sending',
      is_read: true, // Group messages are considered read by the sender
      // Add any other properties your message objects have
    };

    // Optimistically add to state
    setMessages(prev => {
      const existingMessages = prev[chatKey] || [];
      return {
        ...prev,
        [chatKey]: [...existingMessages, newMessage]
      };
    });

    try {
      // Attempt to send via MQTT if connected
      if (mqttConnected) {
        // Publish to the group topic
        const groupTopic = MQTT_CONFIG.TOPICS.GROUP_MESSAGES(groupId);
        
        // Create the message payload
        const payload = {
          type: 'group_message',
          messageId: tempMessageId,
          senderId: currentUser.id,
          groupId: groupId,
          content: content,
          timestamp: timestamp
        };
        
        // Send via MQTT
        await mqttService.publishMessage(groupTopic, payload);
        
        // Update status to 'sent' in local state
        setMessages(prev => {
          const chatMessages = prev[chatKey] || [];
          return {
            ...prev,
            [chatKey]: chatMessages.map(msg => 
              msg.id === tempMessageId 
                ? { ...msg, status: 'sent', timestamp: timestamp }
                : msg
            )
          };
        });
        
        console.log('Group message sent via MQTT');
        return true;
      } else {
        // Fall back to REST API
        const response = await api.post(`/messages/group/${groupId}`, {
          content: content
        });
        
        // Update the message in state with the server response
        if (response.data && response.data.id) {
          setMessages(prev => {
            const chatMessages = prev[chatKey] || [];
            return {
              ...prev,
              [chatKey]: chatMessages.map(msg => 
                msg.id === tempMessageId 
                  ? { ...msg, id: response.data.id, status: 'sent', timestamp: response.data.timestamp || timestamp }
                  : msg
              )
            };
          });
        }
        
        console.log('Group message sent via REST API');
        return true;
      }
    } catch (error) {
      console.error('Error sending group message:', error);
      
      // Update status to 'failed' in local state
      setMessages(prev => {
        const chatMessages = prev[chatKey] || [];
        return {
          ...prev,
          [chatKey]: chatMessages.map(msg => 
            msg.id === tempMessageId 
              ? { ...msg, status: 'failed' }
              : msg
          )
        };
      });
      
      return false;
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
    loadMessages,
    refreshMessages,
    sendMessage,
    sendGroupMessage,
    loadGroupMessages,
    refreshGroupMessages,
    markAsRead,
    mqttConnected,
    getPreservedContent
  };

  return (
    <MessagesContext.Provider value={value}>
      {children}
    </MessagesContext.Provider>
  );
}