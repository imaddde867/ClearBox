import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useGroups } from '../contexts/GroupsContext';
import { useMessages } from '../contexts/MessagesContext';
import { useAuth } from '../contexts/AuthContext';
import { useContacts } from '../contexts/ContactsContext';
import EmojiPicker from 'emoji-picker-react';
import './GroupChat.css';
import './EmojiPicker.css';

function GroupChat() {
  const [message, setMessage] = useState('');
  const [showGroupDetails, setShowGroupDetails] = useState(false);
  const [showNewGroup, setShowNewGroup] = useState(false);
  const [newGroupName, setNewGroupName] = useState('');
  const [selectedContact, setSelectedContact] = useState(null);
  const [creatingGroup, setCreatingGroup] = useState(false);
  const [addingMember, setAddingMember] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState({ type: '', text: '' });
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [emojiSearchTerm, setEmojiSearchTerm] = useState('');
  const [activeEmojiCategory, setActiveEmojiCategory] = useState('all');
  const messagesEndRef = useRef(null);
  const emojiButtonRef = useRef(null);
  const emojiPickerRef = useRef(null);
  const messageInputRef = useRef(null);
  
  const { currentUser } = useAuth();
  const { contacts, refreshContacts } = useContacts();
  const { 
    groups, 
    activeGroup, 
    setActiveGroup, 
    groupMembers, 
    createGroup, 
    addGroupMember,
    deleteGroup,
    leaveGroup,
    loading: groupsLoading 
  } = useGroups();
  const { 
    messages, 
    sendGroupMessage, 
    loadGroupMessages, 
    refreshGroupMessages,
    loading: messagesLoading 
  } = useMessages();

  // Clear feedback message after 3 seconds
  useEffect(() => {
    if (feedbackMessage.text) {
      const timer = setTimeout(() => {
        setFeedbackMessage({ type: '', text: '' });
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [feedbackMessage]);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, activeGroup]);

  // Load messages when active group changes
  useEffect(() => {
    if (activeGroup) {
      loadGroupMessages(activeGroup);
    }
  }, [activeGroup, loadGroupMessages]);

  // Handle sending a message
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim() || !activeGroup) return;

    try {
      await sendGroupMessage(activeGroup, message);
      setMessage('');
      // Close emoji picker if open
      if (showEmojiPicker) {
        setShowEmojiPicker(false);
      }
    } catch (err) {
      console.error('Error sending group message:', err);
      setFeedbackMessage({ 
        type: 'error', 
        text: 'Failed to send message. Please try again.' 
      });
    }
  };
  
  // Handle emoji selection
  const onEmojiClick = useCallback(({ emoji }) => {
    setMessage(prev => prev + emoji);
    messageInputRef.current?.focus();
  }, []);
  
  // Close emoji picker when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        showEmojiPicker &&
        emojiPickerRef.current && 
        !emojiPickerRef.current.contains(event.target) &&
        emojiButtonRef.current &&
        !emojiButtonRef.current.contains(event.target)
      ) {
        setShowEmojiPicker(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showEmojiPicker]);
  
  // Filter emojis based on search and category
  const filteredEmojis = useCallback(() => {
    // This is a simplified version - in a real app, you'd have a proper emoji dataset
    const commonEmojis = [
      { emoji: '😊', name: 'Smiling Face with Smiling Eyes', category: 'smileys' },
      { emoji: '😂', name: 'Face with Tears of Joy', category: 'smileys' },
      { emoji: '❤️', name: 'Red Heart', category: 'symbols' },
      { emoji: '👍', name: 'Thumbs Up', category: 'people' },
      { emoji: '🔥', name: 'Fire', category: 'symbols' },
      { emoji: '🎉', name: 'Party Popper', category: 'activities' },
      { emoji: '🙏', name: 'Folded Hands', category: 'people' },
      { emoji: '😍', name: 'Smiling Face with Heart-Eyes', category: 'smileys' },
      { emoji: '🤔', name: 'Thinking Face', category: 'smileys' },
      { emoji: '👋', name: 'Waving Hand', category: 'people' },
      { emoji: '🌟', name: 'Glowing Star', category: 'symbols' },
      { emoji: '🥰', name: 'Smiling Face with Hearts', category: 'smileys' },
      { emoji: '😭', name: 'Loudly Crying Face', category: 'smileys' },
      { emoji: '🤣', name: 'Rolling on the Floor Laughing', category: 'smileys' },
      { emoji: '🙄', name: 'Face with Rolling Eyes', category: 'smileys' },
      { emoji: '👀', name: 'Eyes', category: 'people' },
      { emoji: '💯', name: 'Hundred Points', category: 'symbols' },
      { emoji: '💕', name: 'Two Hearts', category: 'symbols' },
      { emoji: '🫡', name: 'Saluting Face', category: 'smileys' },
      { emoji: '🤗', name: 'Hugging Face', category: 'smileys' }
    ];
    
    return commonEmojis
      .filter(emoji => {
        // Filter by search term
        if (emojiSearchTerm) {
          return emoji.name.toLowerCase().includes(emojiSearchTerm.toLowerCase());
        }
        
        // Filter by category
        if (activeEmojiCategory !== 'all') {
          return emoji.category === activeEmojiCategory;
        }
        
        return true;
      });
  }, [emojiSearchTerm, activeEmojiCategory]);

  // Create a new group
  const handleCreateGroup = async (e) => {
    e.preventDefault();
    if (!newGroupName.trim() || creatingGroup) return;

    setCreatingGroup(true);
    try {
      await createGroup(newGroupName);
      setNewGroupName('');
      setShowNewGroup(false);
      setFeedbackMessage({ 
        type: 'success', 
        text: `Group "${newGroupName}" created successfully!` 
      });
    } catch (err) {
      console.error('Error creating group:', err);
      setFeedbackMessage({ 
        type: 'error', 
        text: 'Failed to create group. Please try again.' 
      });
    } finally {
      setCreatingGroup(false);
    }
  };

  // Add a contact to current group
  const handleAddMember = async () => {
    if (!selectedContact || !activeGroup || addingMember) return;

    setAddingMember(true);
    try {
      await addGroupMember(activeGroup, selectedContact);
      const contactName = contacts.find(c => c.id === Number(selectedContact))?.username || 'Contact';
      setFeedbackMessage({ 
        type: 'success', 
        text: `${contactName} added to the group!` 
      });
      setSelectedContact(null);
      // Refresh contact list
      refreshContacts();
    } catch (err) {
      console.error('Error adding member to group:', err);
      setFeedbackMessage({ 
        type: 'error', 
        text: 'Failed to add member. Please try again.' 
      });
    } finally {
      setAddingMember(false);
    }
  };

  // Delete current group
  const handleDeleteGroup = async () => {
    if (!activeGroup) return;
    
    if (window.confirm('Are you sure you want to delete this group?')) {
      try {
        const groupName = groups.find(g => g.id === activeGroup)?.name;
        await deleteGroup(activeGroup);
        setFeedbackMessage({ 
          type: 'success', 
          text: `Group "${groupName}" deleted!` 
        });
        setShowGroupDetails(false);
      } catch (err) {
        console.error('Error deleting group:', err);
        setFeedbackMessage({ 
          type: 'error', 
          text: 'Failed to delete group. Please try again.' 
        });
      }
    }
  };

  // Leave current group
  const handleLeaveGroup = async () => {
    if (!activeGroup) return;
    
    if (window.confirm('Are you sure you want to leave this group?')) {
      try {
        const groupName = groups.find(g => g.id === activeGroup)?.name;
        await leaveGroup(activeGroup);
        setFeedbackMessage({ 
          type: 'success', 
          text: `You left the group "${groupName}"` 
        });
        setShowGroupDetails(false);
      } catch (err) {
        console.error('Error leaving group:', err);
        setFeedbackMessage({ 
          type: 'error', 
          text: 'Failed to leave group. Please try again.' 
        });
      }
    }
  };

  // Get current group's messages
  const activeGroupMessages = activeGroup ? (messages[`group-${activeGroup}`] || []) : [];

  // Get current group object
  const currentGroup = groups.find(g => g.id === activeGroup);
  
  // Check if current user is the creator of the active group
  const isCreator = currentGroup?.creator_id === currentUser?.id;

  // Get members of current group
  const currentGroupMembers = groupMembers[activeGroup] || [];

  // Format timestamp for messages
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Format date to show in message groups
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString();
    }
  };

  // Group messages by date for better visual organization
  const groupMessagesByDate = (messages) => {
    const groups = {};
    messages.forEach(msg => {
      const date = new Date(msg.timestamp || msg.created_at).toDateString();
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push(msg);
    });
    return groups;
  };

  const messagesByDate = groupMessagesByDate(activeGroupMessages);

  return (
    <div className="chat-container">
      {/* Feedback message */}
      {feedbackMessage.text && (
        <div className={`feedback-message ${feedbackMessage.type}`}>
          {feedbackMessage.text}
        </div>
      )}
    
      {/* Groups sidebar */}
      <div className="contacts-sidebar">
        <div className="sidebar-header">
          <h2>Groups</h2>
          <button 
            className="new-group-button" 
            onClick={() => setShowNewGroup(!showNewGroup)}
          >
            {showNewGroup ? (
              <>
                <span className="icon">✕</span>
                <span>Cancel</span>
              </>
            ) : (
              <>
                <span className="icon">+</span>
                <span>New Group</span>
              </>
            )}
          </button>
        </div>
        
        {/* New group form */}
        {showNewGroup && (
          <form className="new-group-form" onSubmit={handleCreateGroup}>
            <input
              type="text"
              placeholder="Group name"
              value={newGroupName}
              onChange={(e) => setNewGroupName(e.target.value)}
              className="new-group-input"
              autoFocus
            />
            <button 
              type="submit" 
              className={`create-group-button ${creatingGroup ? 'loading' : ''}`}
              disabled={creatingGroup || !newGroupName.trim()}
            >
              {creatingGroup ? 'Creating...' : 'Create Group'}
            </button>
          </form>
        )}
        
        {/* Groups list */}
        <div className="groups-list">
          {groupsLoading ? (
            <div className="loading-indicator">
              <div className="spinner"></div>
              <span>Loading groups...</span>
            </div>
          ) : groups.length === 0 ? (
            <div className="no-groups">
              <div className="empty-state-icon">👥</div>
              <p>No groups yet</p>
              <p>Create a new group to start chatting with multiple contacts at once.</p>
            </div>
          ) : (
            groups.map(group => (
              <div
                key={group.id}
                className={`group-item ${activeGroup === group.id ? 'active' : ''}`}
                onClick={() => setActiveGroup(group.id)}
              >
                <div className="group-avatar">
                  {group.name.charAt(0).toUpperCase()}
                </div>
                <div className="group-info">
                  <div className="group-name">{group.name}</div>
                  <div className="group-meta">
                    {group.creator_id === currentUser?.id ? (
                      <div className="group-role">Creator</div>
                    ) : (
                      <div className="group-member-count">
                        {groupMembers[group.id]?.length || 0} members
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Chat area */}
      <div className="chat-area">
        {activeGroup ? (
          <>
            {/* Group chat header */}
            <div className="chat-header">
              <div className="header-group-info">
                <div className="header-group-avatar">
                  {currentGroup?.name.charAt(0).toUpperCase()}
                </div>
                <div>
                  <div className="header-group-name">{currentGroup?.name || 'Group Chat'}</div>
                  <div className="header-group-meta">
                    {currentGroupMembers.length} members
                  </div>
                </div>
              </div>
              <button 
                className="group-details-button"
                onClick={() => setShowGroupDetails(!showGroupDetails)}
              >
                {showGroupDetails ? 'Hide Details' : 'Group Details'}
              </button>
            </div>

            {/* Group details sidebar */}
            {showGroupDetails && (
              <div className="group-details-sidebar">
                <h3>Group Members</h3>
                <div className="group-members-list">
                  {currentGroupMembers.map(member => (
                    <div key={member.id} className="group-member-item">
                      <div className="member-avatar">
                        {member.user.username.charAt(0).toUpperCase()}
                      </div>
                      <div className="member-name">
                        {member.user.username}
                        {member.user.id === currentGroup?.creator_id && (
                          <span className="creator-badge">Creator</span>
                        )}
                        {member.user.id === currentUser?.id && (
                          <span className="self-badge">You</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Add member form for group creators */}
                {isCreator && (
                  <div className="add-member-section">
                    <h4>Add Member</h4>
                    <select
                      value={selectedContact || ''}
                      onChange={(e) => setSelectedContact(e.target.value ? Number(e.target.value) : null)}
                      className="contact-select"
                    >
                      <option value="">Select a contact</option>
                      {contacts.length === 0 ? (
                        <option disabled>No contacts available</option>
                      ) : (
                        contacts.map(contact => {
                          // Check if contact is already a member
                          const isMember = currentGroupMembers.some(
                            member => member.user.id === contact.id
                          );
                          return !isMember && (
                            <option key={contact.id} value={contact.id}>
                              {contact.username}
                            </option>
                          );
                        })
                      )}
                    </select>
                    <button 
                      onClick={handleAddMember}
                      disabled={!selectedContact || addingMember}
                      className={`add-member-button ${addingMember ? 'loading' : ''}`}
                    >
                      {addingMember ? 'Adding...' : 'Add to Group'}
                    </button>
                  </div>
                )}

                {/* Group management buttons */}
                <div className="group-management">
                  {isCreator ? (
                    <button 
                      onClick={handleDeleteGroup}
                      className="delete-group-button"
                    >
                      <span className="icon">🗑️</span>
                      <span>Delete Group</span>
                    </button>
                  ) : (
                    <button 
                      onClick={handleLeaveGroup}
                      className="leave-group-button"
                    >
                      <span className="icon">👋</span>
                      <span>Leave Group</span>
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Messages container */}
            <div className={`messages-container ${showGroupDetails ? 'with-sidebar' : ''}`}>
              {messagesLoading ? (
                <div className="loading-indicator">
                  <div className="spinner"></div>
                  <span>Loading messages...</span>
                </div>
              ) : (
                activeGroupMessages.length === 0 ? (
                  <div className="no-messages">
                    <div className="empty-state-icon">💬</div>
                    <p>No messages yet</p>
                    <p>Be the first to start a conversation!</p>
                  </div>
                ) : (
                  Object.entries(messagesByDate).map(([date, msgs]) => (
                    <div key={date} className="message-date-group">
                      <div className="date-divider">
                        <span>{formatDate(msgs[0].timestamp || msgs[0].created_at)}</span>
                      </div>
                      {msgs.map(msg => (
                        <div
                          key={msg.id}
                          className={`message ${msg.sender_id === currentUser?.id ? 'own-message' : 'other-message'}`}
                        >
                          {/* Show sender name for messages not from current user */}
                          {msg.sender_id !== currentUser?.id && (
                            <div className="message-sender">
                              {currentGroupMembers.find(m => m.user.id === msg.sender_id)?.user.username || 'User'}
                            </div>
                          )}
                          <div className="message-content">{msg.content}</div>
                          <div className="message-time">
                            {formatTime(msg.timestamp || msg.created_at)}
                          </div>
                        </div>
                      ))}
                    </div>
                  ))
                )
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Message input */}
            <form className="message-input-container" onSubmit={handleSendMessage}>
              <button
                type="button"
                ref={emojiButtonRef}
                className="emoji-button"
                onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                title={showEmojiPicker ? "Close emoji picker" : "Open emoji picker"}
                aria-label={showEmojiPicker ? "Close emoji picker" : "Open emoji picker"}
              >
                {showEmojiPicker ? "✖️" : "😊"}
              </button>
              {showEmojiPicker && (
                <div className="emoji-picker-container" ref={emojiPickerRef}>
                  <div className="custom-emoji-picker">
                    <div className="emoji-search">
                      <input
                        type="text"
                        placeholder="Search emoji..."
                        autoFocus
                        value={emojiSearchTerm}
                        onChange={(e) => setEmojiSearchTerm(e.target.value)}
                      />
                    </div>
                    <div className="emoji-categories">
                      <button
                        className={`emoji-category ${activeEmojiCategory === 'all' ? 'active' : ''}`}
                        onClick={() => setActiveEmojiCategory('all')}
                        title="All Emojis"
                      >
                        😊
                      </button>
                      <button
                        className={`emoji-category ${activeEmojiCategory === 'smileys' ? 'active' : ''}`}
                        onClick={() => setActiveEmojiCategory('smileys')}
                        title="Smileys & Emotion"
                      >
                        😀
                      </button>
                      <button
                        className={`emoji-category ${activeEmojiCategory === 'people' ? 'active' : ''}`}
                        onClick={() => setActiveEmojiCategory('people')}
                        title="People & Body"
                      >
                        👋
                      </button>
                      <button
                        className={`emoji-category ${activeEmojiCategory === 'symbols' ? 'active' : ''}`}
                        onClick={() => setActiveEmojiCategory('symbols')}
                        title="Symbols"
                      >
                        💡
                      </button>
                    </div>
                    <div className="emoji-list">
                      {filteredEmojis().length > 0 ? (
                        filteredEmojis().map((emoji, index) => (
                          <button
                            key={index}
                            className="emoji-item"
                            onClick={() => {
                              onEmojiClick({emoji: emoji.emoji});
                              setEmojiSearchTerm(''); // Clear search after selection
                            }}
                            title={emoji.name}
                          >
                            {emoji.emoji}
                          </button>
                        ))
                      ) : (
                        <div className="no-emoji-results">No emojis found</div>
                      )}
                    </div>
                  </div>
                </div>
              )}
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
                className="message-input"
                ref={messageInputRef}
              />
              <button 
                type="submit" 
                className="send-button"
                disabled={!message.trim()}
              >
                Send
              </button>
            </form>
          </>
        ) : (
          <div className="no-chat-selected">
            <div className="empty-state-icon">👥</div>
            <div className="empty-state-title">Welcome to Group Chat</div>
            <div className="empty-state-description">Select a group from the sidebar or create a new one to start chatting</div>
            {groups.length === 0 && (
              <button 
                onClick={() => setShowNewGroup(true)}
                className="create-first-group"
              >
                <span className="icon">+</span>
                <span>Create Your First Group</span>
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default GroupChat;