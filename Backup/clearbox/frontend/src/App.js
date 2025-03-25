import React, { useState, useEffect, useRef, useMemo } from 'react';
import { 
  BrowserRouter as Router, 
  Routes, 
  Route, 
  Navigate, 
  Link,
} from 'react-router-dom';
import EmojiPicker from 'emoji-picker-react';
import { useAuth } from './contexts/AuthContext';
import { useContacts } from './contexts/ContactsContext';
import { useMessages } from './contexts/MessagesContext';
import { useNotifications } from './contexts/NotificationsContext';
import api from './services/api';
import './App.css';

// MessageItem component with better content handling
const MessageItem = ({ message, currentUserId, formatTime }) => {
  const isSent = message.sender_id === currentUserId;
  
  // Ensure we have proper message content - handle decryption error cases
  const displayContent = () => {
    if (!message.content) {
      return "No message content";
    }
    
    // Handle decryption errors more gracefully
    if (message.content === "[Encrypted message]" || message.content.includes("Decryption error")) {
      return "Message couldn't be decrypted";
    }
    
    return message.content;
  };
  
  // Improved regex for detecting emojis (more comprehensive)
  const isSingleEmoji = () => {
    // Match a single emoji (including compound emojis with ZWJ, skin tone modifiers, etc.)
    // This is more comprehensive than the previous regex
    const emojiRegex = /^(?:\p{Emoji_Presentation}|\p{Emoji}\uFE0F)(?:\u200D(?:\p{Emoji_Presentation}|\p{Emoji}\uFE0F))*(?:\p{Emoji_Modifier})?$/u;
    return displayContent().trim().length <= 3 && emojiRegex.test(displayContent().trim());
  };
  
  const singleEmoji = isSingleEmoji();
  
  return (
    <div className={`message ${isSent ? 'sent' : 'received'} ${message.failed ? 'failed' : ''} ${singleEmoji ? 'single-emoji' : ''}`}>
      <div className={`message-content ${singleEmoji ? 'emoji-content' : ''}`}>
        {displayContent()}
      </div>
      <div className="message-meta">
        <span className="message-time">
          {formatTime(message.timestamp || message.created_at || new Date())}
        </span>
        {isSent && (
          <span className="message-status">
            {message.failed ? 'Failed to send' : 'Sent'}
          </span>
        )}
      </div>
    </div>
  );
};

// Placeholder components - these would be imported from separate component files
const LandingPage = () => {
  // Check if the user was redirected after deleting their account
  const [showDeletedMessage, setShowDeletedMessage] = useState(false);
  
  useEffect(() => {
    // Check for the deleted parameter in the URL
    const params = new URLSearchParams(window.location.search);
    if (params.get('deleted') === 'true') {
      setShowDeletedMessage(true);
      
      // Clear the parameter from the URL
      window.history.replaceState(null, '', '/');
      
      // Hide the message after 5 seconds
      setTimeout(() => {
        setShowDeletedMessage(false);
      }, 5000);
    }
  }, []);
  
  return (
    <div className="landing-page">
      {/* Show success message when account is deleted */}
      {showDeletedMessage && (
        <div className="account-deleted-message">
          <div className="container">
            <p>Your account has been successfully deleted. We're sorry to see you go!</p>
            <button onClick={() => setShowDeletedMessage(false)}>×</button>
          </div>
        </div>
      )}
      
      {/* Header - Sticky */}
      <header className="landing-header">
        <div className="container">
          <div className="logo">
            <h1>ClearBox</h1>
            <span className="logo-icon">🔒</span>
          </div>
          <div className="auth-buttons">
            <Link to="/login" className="button-small">Log In</Link>
            <Link to="/signup" className="button accent">Sign Up</Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">Secure Messaging for the Modern World</h1>
            <p className="hero-subtitle">A GDPR-compliant messaging app with end-to-end encryption, keeping your conversations private</p>
            <div className="hero-cta">
              <Link to="/signup" className="button accent large">Get Started</Link>
              <a href="#features" className="button outline large">Learn More</a>
            </div>
          </div>
          <div className="hero-visual">
            <div className="app-mockup">
              <div className="mockup-screen">
                <div className="mockup-message sent">
                  <div className="message-content">Hello! Your messages are secure with ClearBox.</div>
                  <div className="message-security">🔒 End-to-end encrypted</div>
                </div>
                <div className="mockup-message received">
                  <div className="message-content">That's great to know! Privacy is important to me.</div>
                  <div className="message-security">🔒 End-to-end encrypted</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <h2 className="section-title">Why Choose ClearBox?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🔐</div>
              <h3>End-to-End Encryption</h3>
              <p>Your messages are secure from sender to recipient, unreadable by anyone in between.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📜</div>
              <h3>GDPR Compliant</h3>
              <p>Meets strict European data protection standards to safeguard your personal information.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Real-Time Messaging</h3>
              <p>Instant message delivery for seamless conversations, no matter where you are.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔄</div>
              <h3>Scalable Infrastructure</h3>
              <p>Built to handle millions of messages with minimal latency, even during peak usage.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🖥️</div>
              <h3>User-Friendly Interface</h3>
              <p>Intuitive design makes secure messaging simple and accessible for everyone.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📁</div>
              <h3>Data Portability</h3>
              <p>Export your data anytime - you always maintain control of your information.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="benefits-section">
        <div className="container">
          <h2 className="section-title">Experience the ClearBox Advantage</h2>
          <div className="benefits-grid">
            <div className="benefit-item">
              <h3>Peace of Mind</h3>
              <p>Rest easy knowing your sensitive conversations are protected by top-tier security protocols.</p>
            </div>
            <div className="benefit-item">
              <h3>Seamless Communication</h3>
              <p>Connect across all your devices with a consistent, synchronized experience.</p>
            </div>
            <div className="benefit-item">
              <h3>Regulatory Compliance</h3>
              <p>Stay compliant with global privacy laws including GDPR, CCPA, and more.</p>
            </div>
            <div className="benefit-item">
              <h3>Digital Sovereignty</h3>
              <p>Maintain control over your data with transparent policies and data portability.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Badges Section */}
      <section className="trust-section">
        <div className="container">
          <div className="trust-badges">
            <div className="trust-badge">
              <div className="badge-icon">🔒</div>
              <div className="badge-text">End-to-End Encrypted</div>
            </div>
            <div className="trust-badge">
              <div className="badge-icon">🇪🇺</div>
              <div className="badge-text">GDPR Compliant</div>
            </div>
            <div className="trust-badge">
              <div className="badge-icon">🛡️</div>
              <div className="badge-text">ISO 27001</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <h2 className="cta-title">Ready to Secure Your Conversations?</h2>
          <p className="cta-subtitle">Join ClearBox today and experience the next generation of secure messaging.</p>
          <div className="cta-buttons">
            <Link to="/signup" className="button accent large">Sign Up Now</Link>
            <Link to="/login" className="button outline large">Log In</Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-column">
              <h3>ClearBox</h3>
              <p>Secure, private messaging for individuals and organizations.</p>
            </div>
            <div className="footer-column">
              <h3>Links</h3>
              <ul>
                <li><Link to="/about">About Us</Link></li>
                <li><Link to="/contact">Contact</Link></li>
                <li><Link to="/privacy-policy">Privacy Policy</Link></li>
                <li><Link to="/terms">Terms of Service</Link></li>
              </ul>
            </div>
            <div className="footer-column">
              <h3>Connect</h3>
              <div className="social-icons">
                <a href="#" className="social-icon">🌐</a>
                <a href="#" className="social-icon">📱</a>
                <a href="#" className="social-icon">📧</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; {new Date().getFullYear()} ClearBox. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setIsLoading(true);
    
    try {
      await login(username, password);
      // Login successful - redirect handled by auth-protected routes
    } catch (error) {
      setErrorMsg(error.response?.data?.detail || 'Failed to log in. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card glass">
        <h2>Log In</h2>
        {errorMsg && <div className="error-message">{errorMsg}</div>}
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input 
              type="text" 
              id="username" 
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input 
              type="password" 
              id="password" 
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="button" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Log In'}
          </button>
        </form>
        <p className="auth-alternate">
          Don't have an account? <Link to="/signup">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

const Signup = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [privacyConsent, setPrivacyConsent] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { signup } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    
    // Validate GDPR consent
    if (!privacyConsent) {
      setErrorMsg('You must accept the Privacy Policy to create an account.');
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Include consent information in signup
      await signup(username, email, password, {
        privacyConsent,
        consentTimestamp: new Date().toISOString()
      });
      setSuccessMsg('Account created successfully! Redirecting to dashboard...');
      // Redirect will be handled by auth-protected routes
    } catch (error) {
      setErrorMsg(error.response?.data?.detail || 'Failed to create account. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card glass">
        <h2>Create Account</h2>
        {errorMsg && <div className="error-message">{errorMsg}</div>}
        {successMsg && <div className="success-message">{successMsg}</div>}
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input 
              type="text" 
              id="username" 
              placeholder="Choose a username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input 
              type="email" 
              id="email" 
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input 
              type="password" 
              id="password" 
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          {/* GDPR Consent Checkboxes */}
          <div className="form-group gdpr-consent">
            <div className="consent-checkbox">
              <input 
                type="checkbox" 
                id="privacy-consent" 
                checked={privacyConsent}
                onChange={(e) => setPrivacyConsent(e.target.checked)}
              />
              <label htmlFor="privacy-consent">
                I have read and agree to the <a href="/privacy-policy" target="_blank">Privacy Policy</a>. 
                We collect your data to provide and improve our services. *
              </label>
            </div>
            <p className="consent-note">* Required field</p>
          </div>
          
          <button 
            type="submit" 
            className="button"
            disabled={isLoading}
          >
            {isLoading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>
        <div className="auth-footer">
          <p>Already have an account? <Link to="/login">Log in</Link></p>
        </div>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const { currentUser, logout, updateProfile } = useAuth();
  const { 
    contacts, 
    contactRequests, 
    searchResults, 
    loading,
    error: contactsError,
    searchUsers,
    sendContactRequest,
    acceptContactRequest,
    rejectContactRequest,
    refreshContacts,
    refreshRequests,
    refreshSentRequests
  } = useContacts();
  
  const { 
    messages, 
    activeChat, 
    loading: messagesLoading, 
    error: messagesError,
    setActiveChat,
    sendMessage,
    refreshMessages
  } = useMessages();
  
  const {
    notifications,
    unreadCount,
    loading: notificationsLoading,
    markNotificationAsRead,
    markAllNotificationsAsRead,
    refreshNotifications
  } = useNotifications();

  const [activeSection, setActiveSection] = useState('messages');
  const [searchTerm, setSearchTerm] = useState('');
  const [newMessage, setNewMessage] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [connectionError, setConnectionError] = useState(false);
  const messageInputRef = useRef(null);
  const emojiPickerRef = useRef(null);
  const emojiButtonRef = useRef(null);
  const [notification, setNotification] = useState(null);
  const messageListRef = useRef(null);
  
  // Add missing variables for the profile section
  const [profileSuccess, setProfileSuccess] = useState('');
  const [profileError, setProfileError] = useState('');
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [editedUsername, setEditedUsername] = useState('');
  const [editedEmail, setEditedEmail] = useState('');
  const [profile, setProfile] = useState({ username: '', email: '' });
  
  // Add missing variables for emoji picker
  const [emojiSearchTerm, setEmojiSearchTerm] = useState('');
  const [activeEmojiCategory, setActiveEmojiCategory] = useState('all');
  const [filteredEmojis, setFilteredEmojis] = useState([]);
  
  // For display, either use the username or extract it from email
  const displayName = currentUser?.username || (currentUser?.email ? currentUser.email.split('@')[0] : 'User');
  const updatedDisplayName = profile.username || displayName;
  
  // Initialize profile data
  useEffect(() => {
    if (currentUser) {
      setProfile({
        username: currentUser.username || '',
        email: currentUser.email || ''
      });
      setEditedUsername(currentUser.username || '');
      setEditedEmail(currentUser.email || '');
    }
  }, [currentUser]);
  
  // Helper functions
  const formatMessageTime = (timestamp) => {
    if (!timestamp) return '';
    
    let date;
    // Handle different timestamp formats
    if (typeof timestamp === 'string') {
      date = new Date(timestamp);
    } else if (timestamp instanceof Date) {
      date = timestamp;
    } else {
      return '';
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) return '';
    
    // Format the time
    const hours = date.getHours();
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const formattedHours = (hours % 12) || 12; // Convert 24h to 12h format
    
    return `${formattedHours}:${minutes} ${ampm}`;
  };

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  };

  // Handle emoji picker
  useEffect(() => {
    if (activeEmojiCategory === 'all' && !emojiSearchTerm) {
      // Populate with default emojis
      setFilteredEmojis([
        { emoji: '😀', name: 'Grinning Face' },
        { emoji: '😊', name: 'Smiling Face with Smiling Eyes' },
        { emoji: '🙂', name: 'Slightly Smiling Face' },
        { emoji: '😍', name: 'Smiling Face with Heart-Eyes' },
        { emoji: '👋', name: 'Waving Hand' },
        { emoji: '👍', name: 'Thumbs Up' },
        { emoji: '❤️', name: 'Red Heart' },
        { emoji: '🔥', name: 'Fire' },
        { emoji: '🎉', name: 'Party Popper' },
        { emoji: '🙏', name: 'Folded Hands' },
        { emoji: '🐱', name: 'Cat Face' },
        { emoji: '🐶', name: 'Dog Face' },
        { emoji: '🍕', name: 'Pizza' },
        { emoji: '🍰', name: 'Shortcake' },
        { emoji: '⚽', name: 'Soccer Ball' },
        { emoji: '🎮', name: 'Video Game' },
        { emoji: '✈️', name: 'Airplane' },
        { emoji: '🏖️', name: 'Beach with Umbrella' },
        { emoji: '💡', name: 'Light Bulb' },
        { emoji: '💯', name: 'Hundred Points' }
      ]);
    } else {
      // Filter emojis based on search term or category
      // This would normally be more complex with a full emoji dataset
      const allEmojis = [
        // Smileys category
        { emoji: '😀', name: 'Grinning Face', category: 'smileys' },
        { emoji: '😊', name: 'Smiling Face with Smiling Eyes', category: 'smileys' },
        { emoji: '🙂', name: 'Slightly Smiling Face', category: 'smileys' },
        { emoji: '😍', name: 'Smiling Face with Heart-Eyes', category: 'smileys' },
        
        // People category
        { emoji: '👋', name: 'Waving Hand', category: 'people' },
        { emoji: '��', name: 'Thumbs Up', category: 'people' },
        { emoji: '🙏', name: 'Folded Hands', category: 'people' },
        { emoji: '🤝', name: 'Handshake', category: 'people' },
        
        // Animals category
        { emoji: '🐱', name: 'Cat Face', category: 'animals' },
        { emoji: '🐶', name: 'Dog Face', category: 'animals' },
        { emoji: '🦊', name: 'Fox', category: 'animals' },
        { emoji: '🐼', name: 'Panda', category: 'animals' },
        
        // Food category
        { emoji: '🍕', name: 'Pizza', category: 'food' },
        { emoji: '🍰', name: 'Shortcake', category: 'food' },
        { emoji: '🍎', name: 'Red Apple', category: 'food' },
        { emoji: '🍔', name: 'Hamburger', category: 'food' },
        
        // Activities category
        { emoji: '⚽', name: 'Soccer Ball', category: 'activities' },
        { emoji: '🎮', name: 'Video Game', category: 'activities' },
        { emoji: '🎨', name: 'Artist Palette', category: 'activities' },
        { emoji: '🎯', name: 'Direct Hit', category: 'activities' },
        
        // Travel category
        { emoji: '✈️', name: 'Airplane', category: 'travel' },
        { emoji: '🏖️', name: 'Beach with Umbrella', category: 'travel' },
        { emoji: '🚗', name: 'Car', category: 'travel' },
        { emoji: '🏔️', name: 'Mountain', category: 'travel' },
        
        // Symbols category
        { emoji: '💡', name: 'Light Bulb', category: 'symbols' },
        { emoji: '💯', name: 'Hundred Points', category: 'symbols' },
        { emoji: '❤️', name: 'Red Heart', category: 'symbols' },
        { emoji: '🔥', name: 'Fire', category: 'symbols' }
      ];
      
      let filteredResults = allEmojis;
      
      // Filter by category if not 'all'
      if (activeEmojiCategory !== 'all') {
        filteredResults = allEmojis.filter(emoji => 
          emoji.category === activeEmojiCategory
        );
      }
      
      // Filter by search term if provided
      if (emojiSearchTerm) {
        const searchLower = emojiSearchTerm.toLowerCase();
        filteredResults = filteredResults.filter(emoji => 
          emoji.name.toLowerCase().includes(searchLower)
        );
      }
      
      setFilteredEmojis(filteredResults);
    }
  }, [activeEmojiCategory, emojiSearchTerm]);

  // Emoji click handler
  const onEmojiClick = ({ emoji }) => {
    if (messageInputRef.current) {
      const cursorPosition = messageInputRef.current.selectionStart;
      const text = newMessage;
      const newText = text.slice(0, cursorPosition) + emoji + text.slice(cursorPosition);
      setNewMessage(newText);
      
      // Focus back on the input
      setTimeout(() => {
        messageInputRef.current.focus();
        messageInputRef.current.selectionStart = cursorPosition + emoji.length;
        messageInputRef.current.selectionEnd = cursorPosition + emoji.length;
      }, 10);
    } else {
      setNewMessage(newMessage + emoji);
    }
    
    // Close the emoji picker
    setShowEmojiPicker(false);
  };

  // Handle keyboard shortcuts
  const handleKeyboardShortcut = (e) => {
    // Ctrl+E or Cmd+E to toggle emoji picker
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
      e.preventDefault();
      setShowEmojiPicker(!showEmojiPicker);
    }
  };

  // Handle notification click
  const handleNotificationClick = (notification) => {
    // Mark as read
    if (!notification.read) {
      markNotificationAsRead(notification.id);
    }
    
    // Handle different notification types
    if (notification.type === 'message' && notification.sender_id) {
      setActiveChat(notification.sender_id);
      setActiveSection('messages');
    } else if (notification.type === 'contact_request') {
      setActiveSection('contacts');
      setShowSearch(false);
    } else if (notification.type === 'contact_accepted') {
      setActiveSection('contacts');
      setShowSearch(false);
    }
    
    // Close notifications dropdown
    setShowNotifications(false);
  };

  // Handle logout
  const handleLogout = () => {
    logout();
    // Redirect to home page instead of login page
    window.location.href = '/';
  };

  // Use useMemo to memoize activeChatMessages to prevent it from changing on every render
  const activeChatMessages = useMemo(() => {
    return activeChat ? (messages[activeChat] || []) : [];
  }, [activeChat, messages]);
  
  // Handle sending a message
  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !activeChat) return;
    
    // First check if we're authenticated
    if (!currentUser) {
      console.error("Cannot send message: Not authenticated");
      setConnectionError(true);
      setTimeout(() => {
        window.location.href = '/login';
      }, 1500);
      return;
    }
    
    // Cache the message and clear input field immediately for better UX
    const messageToSend = newMessage.trim();
    setNewMessage(''); // Clear input immediately
    
    // Scroll to bottom immediately for better UX
    setTimeout(scrollToBottom, 10);
    
    // Send the message
    sendMessage(activeChat, messageToSend)
      .catch(error => {
        console.error("Error sending message:", error);
        // Show error message to user
        setNotification({
          message: `Failed to send message: ${error.message || 'Please try again'}`,
          type: 'error',
          timeout: 5000
        });
        
        // If there's an authentication error, redirect to login
        if (error.message?.includes('Authentication') || error.message?.includes('log in')) {
          setTimeout(() => {
            window.location.href = '/login';
          }, 2000);
        }
      });
  };

  // Handle searching for users
  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchTerm(query);
    if (query.length >= 2) {
      searchUsers(query);
    }
  };

  // Send contact request handler
  const handleSendContactRequest = async (userId) => {
    try {
      const result = await sendContactRequest(userId);
      if (result.success) {
        setNotification({
          message: 'Contact request sent successfully',
          type: 'success',
          timeout: 3000
        });
      } else {
        setContactRequestError(result.message || 'Failed to send contact request');
      }
    } catch (error) {
      console.error('Error sending contact request:', error);
      setContactRequestError('Failed to send request. Please try again.');
    }
  };

  // Get contact details helper
  const getContactDetails = (contactId) => {
    return contacts.find(contact => contact.id === contactId) || { username: 'Unknown User' };
  };

  // Update profile handler
  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setProfileError('');
    setProfileSuccess('');
    
    try {
      await updateProfile({
        username: editedUsername,
        email: editedEmail
      });
      
      setProfile({
        username: editedUsername,
        email: editedEmail
      });
      
      setProfileSuccess('Profile updated successfully');
      setIsEditingProfile(false);
    } catch (error) {
      console.error('Error updating profile:', error);
      setProfileError(error.response?.data?.detail || 'Failed to update profile');
    }
  };

  // Edit profile handler
  const handleEditProfileClick = () => {
    setEditedUsername(profile.username);
    setEditedEmail(profile.email);
    setIsEditingProfile(true);
  };

  // Add a state for contact request error feedback
  const [contactRequestError, setContactRequestError] = useState('');
  const [acceptRequestError, setAcceptRequestError] = useState('');
  const [acceptRequestSuccess, setAcceptRequestSuccess] = useState('');

  // Add loading state for contact requests
  const [acceptingRequest, setAcceptingRequest] = useState(null);
  const [rejectingRequest, setRejectingRequest] = useState(null);

  // Use a ref to track if initial data has been loaded
  const initialDataLoadedRef = useRef(false);

  // Add a useEffect to ensure we track when contacts finish loading
  useEffect(() => {
    // If we have contacts data and the loading is complete, mark data as loaded
    if (contacts?.length > 0 && !loading.contacts) {
      initialDataLoadedRef.current = true;
    }
  }, [contacts, loading.contacts]);

  // Add a helper function to determine if contacts data is actually in a loading state
  const isContactsLoading = () => {
    // Consider contacts as loading only if:
    // 1. loading.contacts is true
    // 2. AND we haven't successfully loaded contacts before
    // 3. AND contacts list is empty
    return loading.contacts && !initialDataLoadedRef.current && contacts.length === 0;
  };

  // Dashboard initialization and auth verification
  useEffect(() => {
    if (!currentUser) {
      console.log("No user data available. User may need to login.");
      return;
    }
    
    console.log("Dashboard mounted with authenticated user:", currentUser.username);
    
    // Load initial data with proper initial load flag
    const loadInitialData = async () => {
      try {
        console.log("Loading initial dashboard data...");
        // Force non-silent loads for first mount
        if (refreshContacts) await refreshContacts(false);
        if (refreshRequests) await refreshRequests(false);
        if (refreshSentRequests) await refreshSentRequests(false);
        if (refreshNotifications) await refreshNotifications();
        
        // Set the ref to true if we have contacts
        if (contacts?.length > 0) {
          initialDataLoadedRef.current = true;
        }
      } catch (error) {
        console.error("Error loading initial data:", error);
      }
    };
    
    loadInitialData();
    
    // Set up a token verification interval to ensure we stay logged in
    const tokenVerificationInterval = setInterval(() => {
      const token = localStorage.getItem('clearboxToken');
      if (!token) {
        console.error("Authentication token missing during verification");
        setConnectionError(true);
        clearInterval(tokenVerificationInterval);
        return;
      }
      
      // Verify token is still valid by making a lightweight API call
      api.get('/profile')
        .catch(error => {
          console.error("Token verification failed:", error);
          if (error.response?.status === 401) {
            setConnectionError(true);
            clearInterval(tokenVerificationInterval);
          }
        });
    }, 60000); // Check every minute
    
    return () => {
      clearInterval(tokenVerificationInterval);
    };
  }, [currentUser, refreshContacts, refreshRequests, refreshSentRequests, refreshNotifications, contacts]);

  // Update the authentication verification useEffect to include missing dependencies
  useEffect(() => {
    if (activeChat) {
      const token = localStorage.getItem('clearboxToken');
      if (!token || !currentUser) {
        console.error("Cannot load messages: Not properly authenticated");
        setConnectionError(true);
        return;
      }
      
      refreshMessages(activeChat);
    }
  }, [activeChat, currentUser, refreshMessages, setConnectionError]);

  // Add notification display rendering if it doesn't exist
  const renderNotification = () => {
    if (!notification) return null;
    
    return (
      <div className={`notification ${notification.type}`}>
        <span>{notification.message}</span>
      </div>
    );
  };

  // Add effect to refresh contacts whenever tab is switched to messages
  useEffect(() => {
    if (activeSection === 'messages' && currentUser) {
      console.log('Switching to messages tab, refreshing contacts...');
      if (refreshContacts) {
        refreshContacts(true); // Silent refresh to avoid loading indicators
      }
    }
  }, [activeSection, currentUser, refreshContacts]);

  // When activeChat changes, ensure we load messages and mark them as read
  useEffect(() => {
    if (activeChat && refreshMessages) {
      console.log(`Loading messages for active chat: ${activeChat}`);
      refreshMessages(activeChat, false); // Not silent, show loading indicator
    }
  }, [activeChat, refreshMessages]);

  // Add a new state for delete account confirmation
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteAccountError, setDeleteAccountError] = useState('');
  const [deleteAccountLoading, setDeleteAccountLoading] = useState(false);

  // Add a delete account handler function
  const handleDeleteAccount = async () => {
    // First check if the user is trying to confirm
    if (!showDeleteConfirm) {
      setShowDeleteConfirm(true);
      return;
    }
    
    setDeleteAccountLoading(true);
    setDeleteAccountError('');
    
    try {
      // Call the delete account endpoint
      await api.delete('/users/account');
      
      // Logout the user
      logout();
      
      // Redirect to home with a message
      window.location.href = '/?deleted=true';
    } catch (error) {
      console.error('Error deleting account:', error);
      setDeleteAccountError(error.response?.data?.detail || 'Failed to delete account. Please try again.');
      setDeleteAccountLoading(false);
      // Keep confirmation dialog open on error
    }
  };

  return (
    <div className="dashboard-container">
      {renderNotification()}
      {connectionError && (
        <div className="connection-error-banner">
          <span>Connection error. Please check your internet connection or try logging in again.</span>
          <button 
            className="button-small"
            onClick={() => window.location.href = '/login'}
          >
            Re-login
          </button>
        </div>
      )}
      <header className="dashboard-header">
        <h2>ClearBox</h2>
        <div className="user-controls">
          <div className="notification-badge" onClick={() => setShowNotifications(!showNotifications)}>
            <span className="notification-icon">🔔</span>
            {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
          </div>
          <span className="username">{displayName}</span>
          <button onClick={handleLogout} className="button-outline">Logout</button>
        </div>
      </header>
      
      {/* Notifications Dropdown */}
      {showNotifications && (
        <div className="notifications-dropdown">
          <div className="notifications-header">
            <h3>Notifications</h3>
            {unreadCount > 0 && (
              <button onClick={markAllNotificationsAsRead} className="button-small">
                Mark all as read
              </button>
            )}
          </div>
          <div className="notifications-list">
            {notifications?.length > 0 ? (
              notifications.map(notification => (
                <div 
                  key={notification.id} 
                  className={`notification-item ${!notification.read ? 'unread' : ''}`}
                  onClick={() => handleNotificationClick(notification)}
                >
                  <div className="notification-content">
                    {notification.type === 'contact_request' && '👤 '}
                    {notification.type === 'contact_accepted' && '✅ '}
                    {notification.type === 'message' && '💬 '}
                    {notification.content}
                  </div>
                  <div className="notification-time">
                    {formatMessageTime(notification.created_at)}
                  </div>
                </div>
              ))
            ) : (
              <p className="no-notifications">No notifications yet</p>
            )}
          </div>
        </div>
      )}
      
      <div className="dashboard-layout">
        <nav className="sidebar">
          <div className="sidebar-header">
            <h3>Navigation</h3>
          </div>
          <ul className="nav-links">
            <li className={activeSection === 'messages' ? 'active' : ''}>
              <button onClick={() => setActiveSection('messages')}>Messages</button>
            </li>
            <li className={activeSection === 'contacts' ? 'active' : ''}>
              <button onClick={() => setActiveSection('contacts')}>
                Contacts
                {contactRequests?.length > 0 && <span className="badge">{contactRequests.length}</span>}
              </button>
            </li>
            <li className={activeSection === 'profile' ? 'active' : ''}>
              <button onClick={() => setActiveSection('profile')}>Profile</button>
            </li>
          </ul>
        </nav>
        
        <main className="main-content">
          {activeSection === 'messages' && (
            <div className="messages-section">
              <div className="messages-layout">
                <div className="contacts-sidebar">
                  <div className="section-header">
                    <h3>Contacts</h3>
                    <button 
                      onClick={() => setShowSearch(!showSearch)} 
                      className="button-small"
                    >
                      {showSearch ? 'Cancel' : 'Add Contact'}
                    </button>
                  </div>
                  
                  {showSearch && (
                    <div className="search-container">
                      <input
                        type="text"
                        placeholder="Search by email or username..."
                        value={searchTerm}
                        onChange={handleSearch}
                        className="search-input"
                      />
                      
                      <div className="search-results">
                        {searchResults?.length > 0 ? (
                          searchResults.map(user => (
                            <div key={user.id} className="search-result-item">
                              <div className="user-info">
                                <span className="username">{user.username || 'Unknown User'}</span>
                                <span className="email">{user.email || 'No email available'}</span>
                              </div>
                              <button 
                                onClick={() => handleSendContactRequest(user.id)}
                                className="button-small"
                              >
                                Add
                              </button>
                            </div>
                          ))
                        ) : (
                          searchTerm.length >= 2 && <p className="no-results">No users found</p>
                        )}
                      </div>
                    </div>
                  )}
                  
                  <div className="contacts-list scrollable">
                    {contacts?.length > 0 ? (
                      contacts.map(contact => (
                        <div 
                          key={contact.id} 
                          className={`contact-item ${activeChat === contact.id ? 'active' : ''}`}
                          onClick={() => setActiveChat(contact.id)}
                        >
                          <div className="contact-info">
                            <div className="username">{contact.username || 'Unknown User'}</div>
                          </div>
                        </div>
                      ))
                    ) : isContactsLoading() ? (
                      <div className="loading-indicator">Loading contacts...</div>
                    ) : (
                      <p className="no-contacts">No contacts yet. Add someone to start chatting!</p>
                    )}
                  </div>
                </div>
                
                <div className="chat-area">
                  {activeChat ? (
                    <>
                      <div className="chat-header">
                        <div className="chat-contact-info">
                          <h3>{getContactDetails(activeChat)?.username}</h3>
                        </div>
                      </div>
                      
                      <div className="messages-container">
                        {messagesLoading ? (
                          <div className="loading-indicator">Loading messages...</div>
                        ) : activeChatMessages.length > 0 ? (
                          <div className="message-list" ref={messageListRef}>
                            {activeChatMessages
                              .slice() // Create a copy to avoid mutating the original array
                              .sort((a, b) => { 
                                // Sort by timestamp, oldest first (newer messages at bottom)
                                const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
                                const timeB = new Date(b.timestamp || b.created_at || 0).getTime();
                                return timeA - timeB;
                              })
                              .map((message) => (
                                <MessageItem 
                                  key={message.id} 
                                  message={message} 
                                  currentUserId={currentUser.id} 
                                  formatTime={formatMessageTime} 
                                />
                              ))}
                          </div>
                        ) : (
                          <div className="empty-chat">No messages yet. Start the conversation!</div>
                        )}
                      </div>
                      
                      <form 
                        className="message-form" 
                        onSubmit={handleSendMessage}
                      >
                        <button
                          type="button"
                          ref={emojiButtonRef}
                          className="emoji-button"
                          onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                          title={showEmojiPicker ? "Close emoji picker" : "Open emoji picker (Ctrl+E)"}
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
                                  className={`emoji-category ${activeEmojiCategory === 'animals' ? 'active' : ''}`}
                                  onClick={() => setActiveEmojiCategory('animals')}
                                  title="Animals & Nature"
                                >
                                  🐱
                                </button>
                                <button 
                                  className={`emoji-category ${activeEmojiCategory === 'food' ? 'active' : ''}`}
                                  onClick={() => setActiveEmojiCategory('food')}
                                  title="Food & Drink"
                                >
                                  🍔
                                </button>
                                <button 
                                  className={`emoji-category ${activeEmojiCategory === 'activities' ? 'active' : ''}`}
                                  onClick={() => setActiveEmojiCategory('activities')}
                                  title="Activities"
                                >
                                  ⚽
                                </button>
                                <button 
                                  className={`emoji-category ${activeEmojiCategory === 'travel' ? 'active' : ''}`}
                                  onClick={() => setActiveEmojiCategory('travel')}
                                  title="Travel & Places"
                                >
                                  ✈️
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
                                {filteredEmojis.length > 0 ? (
                                  filteredEmojis.map((emoji, index) => (
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
                          value={newMessage}
                          onChange={(e) => setNewMessage(e.target.value)}
                          placeholder="Type a message..."
                          ref={messageInputRef}
                          onKeyDown={(e) => {
                            if (e.key === 'Escape' && showEmojiPicker) {
                              setShowEmojiPicker(false);
                              e.preventDefault();
                            }
                            handleKeyboardShortcut(e);
                          }}
                        />
                        <button 
                          type="submit" 
                          disabled={!newMessage.trim()}
                        >
                          Send
                        </button>
                      </form>
                    </>
                  ) : (
                    <div className="empty-chat">
                      <p>Select a contact to start chatting</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
          
          {activeSection === 'contacts' && (
            <div className="contacts-section">
              <div className="tabs">
                <button 
                  className={`tab ${!showSearch ? 'active' : ''}`} 
                  onClick={() => setShowSearch(false)}
                >
                  My Contacts
                </button>
                <button 
                  className={`tab ${showSearch ? 'active' : ''}`} 
                  onClick={() => setShowSearch(true)}
                >
                  Find Users
                </button>
              </div>
              
              {showSearch ? (
                <div className="search-users-section">
                  <div className="search-bar">
                    <input
                      type="text"
                      placeholder="Search by email or username..."
                      value={searchTerm}
                      onChange={handleSearch}
                      autoFocus
                    />
                  </div>
                  
                  {/* Show error message if there is one */}
                  {contactRequestError && (
                    <div className="error-message">{contactRequestError}</div>
                  )}
                  
                  <div className="search-results-container">
                    {loading.search ? (
                      <div className="loading-indicator">Searching...</div>
                    ) : searchResults?.length > 0 ? (
                      <div className="search-results-list">
                        {searchResults.map(user => (
                          <div key={user.id} className="user-card">
                            <div className="user-info">
                              <h4>{user.username || 'Unknown User'}</h4>
                              <p>{user.email || 'No email available'}</p>
                            </div>
                            <button 
                              onClick={() => handleSendContactRequest(user.id)}
                              className="button-small"
                              title="Send contact request"
                            >
                              Add Contact
                            </button>
                          </div>
                        ))}
                      </div>
                    ) : (
                      searchTerm.length >= 2 && 
                      <div className="no-results">
                        <p>No users found matching "{searchTerm}"</p>
                        <p className="search-tip">Try a different search term or check the spelling</p>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="contacts-management">
                  <div className="contact-requests-section">
                    <h3>Contact Requests</h3>
                    {acceptRequestError && <div className="error-message">{acceptRequestError}</div>}
                    {acceptRequestSuccess && <div className="success-message">{acceptRequestSuccess}</div>}
                    <div className="contact-requests-list">
                      {contactRequests.map(request => (
                        <div key={request.id} className="contact-request-card">
                          <div className="user-info">
                            <h4>{request.from_user?.username || 'Unknown User'}</h4>
                            <p>{request.from_user?.email || 'No email available'}</p>
                          </div>
                          <div className="request-actions">
                            <button 
                              onClick={async () => {
                                try {
                                  setAcceptRequestError('');
                                  setAcceptRequestSuccess('');
                                  // Set loading for this specific request
                                  setAcceptingRequest(request.id);
                                  
                                  const result = await acceptContactRequest(request.id);
                                  if (result && result.success) {
                                    setAcceptRequestSuccess('Contact request accepted successfully!');
                                    // Refresh contacts list
                                    refreshContacts && refreshContacts();
                                    // Clear success message after 3 seconds
                                    setTimeout(() => setAcceptRequestSuccess(''), 3000);
                                  } else if (result && !result.success) {
                                    setAcceptRequestError(result.message || 'Failed to accept contact request');
                                  }
                                } catch (error) {
                                  console.error('Error accepting contact request:', error);
                                  setAcceptRequestError('Failed to accept request. Please try again.');
                                } finally {
                                  // Clear loading state
                                  setAcceptingRequest(null);
                                }
                              }}
                              className={`button-small ${acceptingRequest === request.id ? 'loading' : ''}`}
                              disabled={acceptingRequest === request.id}
                              title="Accept contact request"
                            >
                              Accept
                            </button>
                            <button 
                              onClick={async () => {
                                try {
                                  setAcceptRequestError('');
                                  setAcceptRequestSuccess('');
                                  // Set loading for this specific request
                                  setRejectingRequest(request.id);
                                  
                                  const result = await rejectContactRequest(request.id);
                                  if (result && result.success) {
                                    setAcceptRequestSuccess('Contact request rejected');
                                    // Clear success message after 3 seconds
                                    setTimeout(() => setAcceptRequestSuccess(''), 3000);
                                  } else if (result && !result.success) {
                                    setAcceptRequestError(result.message || 'Failed to reject contact request');
                                  }
                                } catch (error) {
                                  console.error('Error rejecting contact request:', error);
                                  setAcceptRequestError('Failed to reject request. Please try again.');
                                } finally {
                                  // Clear loading state
                                  setRejectingRequest(null);
                                }
                              }}
                              className={`button-small outline ${rejectingRequest === request.id ? 'loading' : ''}`}
                              disabled={rejectingRequest === request.id}
                              title="Decline contact request"
                            >
                              Decline
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="my-contacts-section">
                    <h3>My Contacts</h3>
                    <div className="contacts-grid">
                      {contacts?.length > 0 ? (
                        contacts.map(contact => (
                          <div key={contact.id} className="contact-card">
                            <div className="contact-info">
                              <div className="username">{contact.username || 'Unknown User'}</div>
                            </div>
                            <button 
                              className="button-small"
                              onClick={() => {
                                setActiveChat(contact.id);
                                setActiveSection('messages');
                              }}
                              title="Start a conversation"
                            >
                              Message
                            </button>
                          </div>
                        ))
                      ) : isContactsLoading() ? (
                        <div className="loading-indicator">Loading contacts...</div>
                      ) : (
                        <p className="no-contacts">You don't have any contacts yet</p>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
          
          {activeSection === 'profile' && (
            <div className="profile-section">
              <h3>Your Profile</h3>
              {profileSuccess && <div className="success-message">{profileSuccess}</div>}
              {profileError && <div className="error-message">{profileError}</div>}
              
              {isEditingProfile ? (
                <form className="profile-edit-form" onSubmit={handleProfileUpdate}>
                  <div className="form-group">
                    <label htmlFor="edit-username">Username</label>
                    <input
                      type="text"
                      id="edit-username"
                      value={editedUsername}
                      onChange={(e) => setEditedUsername(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="edit-email">Email</label>
                    <input
                      type="email"
                      id="edit-email"
                      value={editedEmail}
                      onChange={(e) => setEditedEmail(e.target.value)}
                      required
                    />
                  </div>
                  <div className="profile-actions">
                    <button type="submit" className="button">Save Changes</button>
                    <button 
                      type="button" 
                      className="button-outline"
                      onClick={() => setIsEditingProfile(false)}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <>
                  <div className="profile-info">
                    <div className="profile-field">
                      <label>Username</label>
                      <p>{updatedDisplayName}</p>
                    </div>
                    <div className="profile-field">
                      <label>Email</label>
                      <p>{profile.email}</p>
                    </div>
                    <div className="profile-actions">
                      <button 
                        className="button-outline"
                        onClick={handleEditProfileClick}
                      >
                        Edit Profile
                      </button>
                      <div className="delete-account-container">
                        <button 
                          className={`button-outline danger ${showDeleteConfirm ? 'confirm' : ''}`}
                          onClick={handleDeleteAccount}
                          disabled={deleteAccountLoading}
                        >
                          {deleteAccountLoading ? 'Deleting...' : (showDeleteConfirm ? 'Confirm Delete' : 'Delete Account')}
                        </button>
                        {showDeleteConfirm && (
                          <button 
                            className="button-outline cancel"
                            onClick={() => setShowDeleteConfirm(false)}
                          >
                            Cancel
                          </button>
                        )}
                      </div>
                    </div>
                    {deleteAccountError && <div className="error-message delete-error">{deleteAccountError}</div>}
                  </div>
                </>
              )}
              
              {/* Data Export Section */}
              <div className="data-export-section">
                <h4>Your Data</h4>
                
                <div className="data-export-options">
                  <div className="export-option">
                    <div className="export-description">
                      <h5>Download Your Data</h5>
                      <p>Get a copy of all your personal data in JSON format</p>
                    </div>
                    <button 
                      className="button-outline export-button"
                      onClick={() => {
                        // Mock data export function - in a real app, this would call an API endpoint
                        const userData = {
                          profile: {
                            username: updatedDisplayName,
                            email: profile.email,
                            id: currentUser.id,
                            created_at: currentUser.created_at || new Date().toISOString()
                          },
                          messages: Object.values(messages).flat(),
                          contacts: contacts
                        };
                        
                        // Create a JSON blob and trigger download
                        const blob = new Blob([JSON.stringify(userData, null, 2)], { type: 'application/json' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `clearbox-user-data-${new Date().toISOString().slice(0, 10)}.json`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        URL.revokeObjectURL(url);
                        
                        setProfileSuccess('Your data export has been generated');
                        setTimeout(() => setProfileSuccess(''), 3000);
                      }}
                    >
                      Download JSON
                    </button>
                  </div>
                </div>
                
                <div className="gdpr-info">
                  <h5>Your Rights Under GDPR</h5>
                  <ul>
                    <li><strong>Right to Access</strong> - You can request a copy of your personal data</li>
                    <li><strong>Right to Rectification</strong> - You can update your data if it's inaccurate</li>
                    <li><strong>Right to Erasure</strong> - You can request deletion of your data</li>
                    <li><strong>Right to Data Portability</strong> - You can request your data in a reusable format</li>
                  </ul>
                  <p>For any questions about your data or privacy, please contact <a href="mailto:contact@clearbox.live">contact@clearbox.live</a></p>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

// Privacy Policy Component
const PrivacyPolicy = () => {
  return (
    <div className="privacy-policy-container">
      <div className="privacy-policy-content">
        <h1>Privacy Policy</h1>
        <p className="last-updated">Last Updated: {new Date().toISOString().slice(0, 10)}</p>
        
        <section>
          <h2>1. Introduction</h2>
          <p>
            Welcome to ClearBox ("we," "our," or "us"). We are committed to protecting your privacy and 
            personal data. This Privacy Policy explains how we collect, use, and safeguard your information 
            when you use our messaging application and services.
          </p>
          <p>
            By using ClearBox, you agree to the collection and use of information in accordance with this policy.
            We collect and process personal data in compliance with the General Data Protection Regulation (GDPR).
          </p>
        </section>
        
        <section>
          <h2>2. Data Controller</h2>
          <p>
            ClearBox operates as the data controller for personal information collected through our services.
            For any questions about your personal data or this privacy policy, please contact us at:
            <br />
            Email: <a href="mailto:contact@clearbox.live">contact@clearbox.live</a>
          </p>
        </section>
        
        <section>
          <h2>3. Information We Collect</h2>
          <p>We collect the following types of information:</p>
          
          <h3>3.1 Information You Provide</h3>
          <ul>
            <li>Account Information: Username and email address when you register</li>
            <li>Profile Information: Any details you choose to add to your profile</li>
            <li>Communications: Messages and content you send through our platform</li>
            <li>Contact Information: Details about contacts you add to your network</li>
          </ul>
          
          <h3>3.2 Information Collected Automatically</h3>
          <ul>
            <li>Device Information: IP address, device type, operating system</li>
            <li>Usage Data: How you interact with our application, features used, time spent</li>
            <li>Connection Information: Login times, session duration, connection status</li>
          </ul>
        </section>
        
        <section>
          <h2>4. How We Use Your Information</h2>
          <p>We use your personal data for the following purposes:</p>
          <ul>
            <li>To provide and maintain our service</li>
            <li>To process and deliver your messages securely</li>
            <li>To authenticate your identity and secure your account</li>
            <li>To respond to your requests or inquiries</li>
            <li>To improve our service through usage analysis</li>
            <li>To detect and prevent fraudulent or abusive activity</li>
            <li>To comply with legal obligations</li>
          </ul>
        </section>
        
        <section>
          <h2>5. Legal Basis for Processing</h2>
          <p>We process your personal data based on the following legal grounds:</p>
          <ul>
            <li>Performance of a contract when providing our service to you</li>
            <li>Your consent, which you can withdraw at any time</li>
            <li>Our legitimate interests, such as improving and securing our service</li>
            <li>Compliance with legal obligations</li>
          </ul>
        </section>
        
        <section>
          <h2>6. Data Retention</h2>
          <p>
            We retain your personal data only for as long as necessary to fulfill the purposes outlined 
            in this Privacy Policy, unless a longer retention period is required or permitted by law.
          </p>
          <p>
            Message content is stored on our servers only until delivery to the recipient's device, after 
            which it may be deleted from our servers but retained on user devices as part of message history.
          </p>
          <p>
            Account information is retained as long as you maintain an active account. Upon account deletion, 
            personal data will be removed or anonymized within 30 days, except where retention is required by law.
          </p>
        </section>
        
        <section>
          <h2>7. Data Security</h2>
          <p>
            We implement appropriate technical and organizational measures to protect your personal data, 
            including end-to-end encryption for messages, secure authentication mechanisms, and regular 
            security assessments.
          </p>
          <p>
            Despite our efforts, no method of transmission over the Internet or electronic storage is 
            100% secure. While we strive to use commercially acceptable means to protect your personal 
            data, we cannot guarantee its absolute security.
          </p>
        </section>
        
        <section>
          <h2>8. Data Sharing and Third Parties</h2>
          <p>We may share your information with:</p>
          <ul>
            <li>Service providers who assist in delivering our services</li>
            <li>Legal authorities when required by law or to protect rights</li>
            <li>Business partners, only with your explicit consent</li>
          </ul>
          <p>
            All third-party service providers are contractually obligated to use your data only for 
            providing services to us and to maintain appropriate security measures.
          </p>
        </section>
        
        <section>
          <h2>9. International Data Transfers</h2>
          <p>
            Your personal data may be processed in countries outside the European Economic Area (EEA). 
            When transferring data internationally, we ensure appropriate safeguards are in place through 
            standard contractual clauses or other valid transfer mechanisms.
          </p>
        </section>
        
        <section>
          <h2>10. Your Data Protection Rights</h2>
          <p>Under the GDPR, you have the following rights:</p>
          <ul>
            <li>Right to Access: Request a copy of your personal data</li>
            <li>Right to Rectification: Correct inaccurate personal data</li>
            <li>Right to Erasure: Request deletion of your personal data</li>
            <li>Right to Data Portability: Receive your data in a structured, machine-readable format</li>
            <li>Right to Object: Object to our processing of your personal data</li>
            <li>Right to Withdraw Consent: Withdraw consent at any time where we rely on consent</li>
          </ul>
          <p>
            To exercise these rights, please contact us at <a href="mailto:contact@clearbox.live">contact@clearbox.live</a>. 
            We will respond to your request within 30 days.
          </p>
        </section>
        
        <section>
          <h2>11. Cookies and Tracking Technologies</h2>
          <p>
            We use cookies and similar tracking technologies to track activity on our service and hold certain information. 
            Cookies are files with small amounts of data which may include an anonymous unique identifier.
          </p>
          <p>
            You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent. 
            However, if you do not accept cookies, you may not be able to use some portions of our service.
          </p>
        </section>
        
        <section>
          <h2>12. Children's Privacy</h2>
          <p>
            Our service is not intended for use by children under the age of 16. We do not knowingly collect 
            personal data from children under 16. If you are a parent or guardian and you are aware that your 
            child has provided us with personal data, please contact us so that we can take necessary actions.
          </p>
        </section>
        
        <section>
          <h2>13. Changes to This Privacy Policy</h2>
          <p>
            We may update our Privacy Policy from time to time. We will notify you of any changes by posting 
            the new Privacy Policy on this page and updating the "Last Updated" date.
          </p>
          <p>
            You are advised to review this Privacy Policy periodically for any changes. Changes to this 
            Privacy Policy are effective when they are posted on this page.
          </p>
        </section>
        
        <section>
          <h2>14. Data Protection Authority</h2>
          <p>
            If you have concerns about our processing of your personal data that we are not able to resolve, 
            you have the right to lodge a complaint with the data protection authority in your jurisdiction.
          </p>
        </section>
        
        <div className="privacy-policy-footer">
          <Link to="/login" className="button">Return to Login</Link>
          <Link to="/" className="button-outline">Back to Home</Link>
        </div>
      </div>
    </div>
  );
};

function App() {
  const { currentUser, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={currentUser ? <Navigate to="/dashboard" /> : <LandingPage />} />
          <Route path="/login" element={currentUser ? <Navigate to="/dashboard" /> : <Login />} />
          <Route path="/signup" element={currentUser ? <Navigate to="/dashboard" /> : <Signup />} />
          <Route path="/dashboard" element={currentUser ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/privacy-policy" element={<PrivacyPolicy />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;