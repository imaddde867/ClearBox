import React, { useState, useEffect } from 'react';
import { useContacts } from '../contexts/ContactsContext';
import { useMessages } from '../contexts/MessagesContext';
import { useAuth } from '../contexts/AuthContext';

function Chat({ contacts }) {
  const [message, setMessage] = useState('');
  const { currentUser } = useAuth();
  const { activeChat, messages, sendMessage, setActiveChat, loading } = useMessages();
  const [searchTerm, setSearchTerm] = useState('');

  // Filter contacts based on search term
  const filteredContacts = contacts.filter(contact =>
    contact.username.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Handle sending a message
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim() || !activeChat) return;

    try {
      await sendMessage(activeChat, message);
      setMessage('');
    } catch (err) {
      console.error('Error sending message:', err);
    }
  };

  // Active chat messages
  const activeChatMessages = activeChat ? (messages[activeChat] || []) : [];

  return (
    <div className="chat-container">
      {/* Sidebar with contacts */}
      <div className="contacts-sidebar">
        <div className="search-container">
          <input
            type="text"
            placeholder="Search contacts..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="contacts-list">
          {filteredContacts.map(contact => (
            <div
              key={contact.id}
              className={`contact-item ${activeChat === contact.id ? 'active' : ''}`}
              onClick={() => setActiveChat(contact.id)}
            >
              <div className="contact-avatar">
                {contact.username.charAt(0).toUpperCase()}
              </div>
              <div className="contact-info">
                <div className="contact-name">{contact.username}</div>
                <div className="contact-last-message">
                  {contact.last_message || 'No messages yet'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chat area */}
      <div className="chat-area">
        {activeChat ? (
          <>
            {/* Chat header */}
            <div className="chat-header">
              {contacts.find(c => c.id === activeChat)?.username || 'Chat'}
            </div>

            {/* Messages container */}
            <div className="messages-container">
              {loading ? (
                <div className="loading-indicator">Loading messages...</div>
              ) : (
                activeChatMessages.length === 0 ? (
                  <div className="no-messages">No messages yet. Start a conversation!</div>
                ) : (
                  activeChatMessages.map(msg => (
                    <div
                      key={msg.id}
                      className={`message ${msg.sender_id === currentUser?.id ? 'own-message' : 'other-message'}`}
                    >
                      <div className="message-content">{msg.content}</div>
                      <div className="message-time">
                        {new Date(msg.timestamp || msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </div>
                    </div>
                  ))
                )
              )}
            </div>

            {/* Message input */}
            <form className="message-input-container" onSubmit={handleSendMessage}>
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
                className="message-input"
              />
              <button type="submit" className="send-button">Send</button>
            </form>
          </>
        ) : (
          <div className="no-chat-selected">
            <div>Select a contact to start chatting</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Chat;