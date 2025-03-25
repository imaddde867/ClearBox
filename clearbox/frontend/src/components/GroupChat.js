import React, { useState, useEffect, useRef } from 'react';
import { useGroups } from '../contexts/GroupsContext';
import { useMessages } from '../contexts/MessagesContext';
import { useAuth } from '../contexts/AuthContext';
import { useContacts } from '../contexts/ContactsContext';
import './GroupChat.css';

function GroupChat() {
  const [message, setMessage] = useState('');
  const [showGroupDetails, setShowGroupDetails] = useState(false);
  const [showNewGroup, setShowNewGroup] = useState(false);
  const [newGroupName, setNewGroupName] = useState('');
  const [selectedContact, setSelectedContact] = useState(null);
  const messagesEndRef = useRef(null);
  
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
    } catch (err) {
      console.error('Error sending group message:', err);
    }
  };

  // Create a new group
  const handleCreateGroup = async (e) => {
    e.preventDefault();
    if (!newGroupName.trim()) return;

    try {
      await createGroup(newGroupName);
      setNewGroupName('');
      setShowNewGroup(false);
    } catch (err) {
      console.error('Error creating group:', err);
    }
  };

  // Add a contact to current group
  const handleAddMember = async () => {
    if (!selectedContact || !activeGroup) return;

    try {
      await addGroupMember(activeGroup, selectedContact);
      setSelectedContact(null);
      // Refresh contact list
      refreshContacts();
    } catch (err) {
      console.error('Error adding member to group:', err);
    }
  };

  // Delete current group
  const handleDeleteGroup = async () => {
    if (!activeGroup) return;
    
    if (window.confirm('Are you sure you want to delete this group?')) {
      try {
        await deleteGroup(activeGroup);
      } catch (err) {
        console.error('Error deleting group:', err);
      }
    }
  };

  // Leave current group
  const handleLeaveGroup = async () => {
    if (!activeGroup) return;
    
    if (window.confirm('Are you sure you want to leave this group?')) {
      try {
        await leaveGroup(activeGroup);
      } catch (err) {
        console.error('Error leaving group:', err);
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

  return (
    <div className="chat-container">
      {/* Groups sidebar */}
      <div className="contacts-sidebar">
        <div className="sidebar-header">
          <h2>Groups</h2>
          <button 
            className="new-group-button" 
            onClick={() => setShowNewGroup(!showNewGroup)}
          >
            {showNewGroup ? 'Cancel' : 'New Group'}
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
            />
            <button type="submit" className="create-group-button">Create</button>
          </form>
        )}
        
        {/* Groups list */}
        <div className="groups-list">
          {groupsLoading ? (
            <div className="loading">Loading groups...</div>
          ) : groups.length === 0 ? (
            <div className="no-groups">No groups yet</div>
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
                  {group.creator_id === currentUser?.id && (
                    <div className="group-role">Creator</div>
                  )}
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
              <div>{currentGroup?.name || 'Group Chat'}</div>
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
                      {contacts.map(contact => {
                        // Check if contact is already a member
                        const isMember = currentGroupMembers.some(
                          member => member.user.id === contact.id
                        );
                        return !isMember && (
                          <option key={contact.id} value={contact.id}>
                            {contact.username}
                          </option>
                        );
                      })}
                    </select>
                    <button 
                      onClick={handleAddMember}
                      disabled={!selectedContact}
                      className="add-member-button"
                    >
                      Add to Group
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
                      Delete Group
                    </button>
                  ) : (
                    <button 
                      onClick={handleLeaveGroup}
                      className="leave-group-button"
                    >
                      Leave Group
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Messages container */}
            <div className={`messages-container ${showGroupDetails ? 'with-sidebar' : ''}`}>
              {messagesLoading ? (
                <div className="loading-indicator">Loading messages...</div>
              ) : (
                activeGroupMessages.length === 0 ? (
                  <div className="no-messages">No messages yet. Start a conversation!</div>
                ) : (
                  activeGroupMessages.map(msg => (
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
                  ))
                )
              )}
              <div ref={messagesEndRef} />
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
            <div>Select a group to start chatting</div>
            {groups.length === 0 && (
              <button 
                onClick={() => setShowNewGroup(true)}
                className="create-first-group"
              >
                Create Your First Group
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default GroupChat; 