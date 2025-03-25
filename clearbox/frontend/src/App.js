import React, { useState, useEffect, useRef, useContext, useMemo } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  Link,
  NavLink,
} from 'react-router-dom';
import EmojiPicker from 'emoji-picker-react';
import { useAuth } from './contexts/AuthContext';
import { useContacts } from './contexts/ContactsContext';
import { useMessages } from './contexts/MessagesContext';
import { useNotifications } from './contexts/NotificationsContext';
import { useGroups } from './contexts/GroupsContext';
import GroupChat from './components/GroupChat';
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

// Add a new component after MessageItem component
const UserAvatar = ({ username, size = '40px' }) => {
  // Generate a consistent color based on the username
  const getColor = (name) => {
    const colors = [
      'linear-gradient(135deg, #556CD6, #3949AB)', // Blue
      'linear-gradient(135deg, #43A047, #2E7D32)', // Green
      'linear-gradient(135deg, #7B1FA2, #6A1B9A)', // Purple
      'linear-gradient(135deg, #EF5350, #D32F2F)', // Red
      'linear-gradient(135deg, #FB8C00, #EF6C00)', // Orange
      'linear-gradient(135deg, #26A69A, #00897B)', // Teal
    ];

    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }

    return colors[Math.abs(hash) % colors.length];
  };

  const initials = username ? username.charAt(0).toUpperCase() : '?';
  const background = getColor(username || '');

  return (
    <div
      className="user-avatar"
      style={{
        width: size,
        height: size,
        background,
        fontSize: `calc(${size} * 0.45)`
      }}
    >
      {initials}
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
    loading: contactsLoading,
    error: contactsError,
    searchUsers,
    sendContactRequest,
    acceptContactRequest,
    rejectContactRequest,
    searchLoading,
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
    refreshMessages,
    isConnected
  } = useMessages();

  const {
    notifications,
    unreadCount,
    loading: notificationsLoading,
    markNotificationAsRead,
    markAllNotificationsAsRead,
    refreshNotifications
  } = useNotifications();

  const {
    groups,
    groupRequests,
    searchGroupResults,
    loading: groupsLoading,
    error: groupsError,
    searchGroups,
    sendGroupRequest,
    acceptGroupRequest,
    rejectGroupRequest,
    searchGroupLoading,
    refreshGroups,
    refreshGroupRequests,
    refreshGroupSentRequests
  } = useGroups();

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

  // Create a ref for the scrollToBottom function to ensure it's accessible in all effects
  const scrollToBottomRef = useRef(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  });

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    scrollToBottomRef.current();
  };

  // Add a specific handler for incoming messages to scroll to bottom immediately
  useEffect(() => {
    // Create a handler specifically for real-time messages
    const handleIncomingMessage = (event) => {
      const data = event.detail;

      // Only process actual messages (not other WebSocket events)
      if (data.type === 'message') {
        // Wait a small amount of time for the message to be processed
        setTimeout(() => {
          // Scroll to bottom immediately for new messages
          scrollToBottomRef.current();
        }, 50);
      }
    };

    // Add event listener
    window.addEventListener('ws-message', handleIncomingMessage);

    // Cleanup on unmount
    return () => {
      window.removeEventListener('ws-message', handleIncomingMessage);
    };
  }, []);

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
        { emoji: '🥰', name: 'Smiling Face with Hearts', category: 'smileys' },
        { emoji: '😂', name: 'Face with Tears of Joy', category: 'smileys' },
        { emoji: '🤣', name: 'Rolling on the Floor Laughing', category: 'smileys' },
        { emoji: '😅', name: 'Grinning Face with Sweat', category: 'smileys' },
        { emoji: '😌', name: 'Relieved Face', category: 'smileys' },
        { emoji: '🥺', name: 'Pleading Face', category: 'smileys' },
        { emoji: '😏', name: 'Smirking Face', category: 'smileys' },
        { emoji: '😴', name: 'Sleeping Face', category: 'smileys' },
        { emoji: '🤔', name: 'Thinking Face', category: 'smileys' },
        { emoji: '🤩', name: 'Star-Struck', category: 'smileys' },
        { emoji: '😎', name: 'Smiling Face with Sunglasses', category: 'smileys' },
        { emoji: '🥳', name: 'Partying Face', category: 'smileys' },
        { emoji: '😤', name: 'Face with Steam From Nose', category: 'smileys' },
        { emoji: '😭', name: 'Loudly Crying Face', category: 'smileys' },
        { emoji: '😱', name: 'Face Screaming in Fear', category: 'smileys' },
        { emoji: '🙄', name: 'Face with Rolling Eyes', category: 'smileys' },
        { emoji: '😬', name: 'Grimacing Face', category: 'smileys' },
        { emoji: '😇', name: 'Smiling Face with Halo', category: 'smileys' },
        { emoji: '🥴', name: 'Woozy Face', category: 'smileys' },
        { emoji: '🤯', name: 'Exploding Head', category: 'smileys' },
        { emoji: '🤫', name: 'Shushing Face', category: 'smileys' },

        // People category
        { emoji: '👋', name: 'Waving Hand', category: 'people' },
        { emoji: '👍', name: 'Thumbs Up', category: 'people' },
        { emoji: '🙏', name: 'Folded Hands', category: 'people' },
        { emoji: '🤝', name: 'Handshake', category: 'people' },
        { emoji: '👏', name: 'Clapping Hands', category: 'people' },
        { emoji: '🙌', name: 'Raising Hands', category: 'people' },
        { emoji: '💪', name: 'Flexed Biceps', category: 'people' },
        { emoji: '🤙', name: 'Call Me Hand', category: 'people' },
        { emoji: '👨‍💻', name: 'Man Technologist', category: 'people' },
        { emoji: '👩‍💻', name: 'Woman Technologist', category: 'people' },
        { emoji: '🧠', name: 'Brain', category: 'people' },
        { emoji: '👑', name: 'Crown', category: 'people' },
        { emoji: '👎', name: 'Thumbs Down', category: 'people' },
        { emoji: '👊', name: 'Oncoming Fist', category: 'people' },
        { emoji: '✌️', name: 'Victory Hand', category: 'people' },
        { emoji: '🤞', name: 'Crossed Fingers', category: 'people' },
        { emoji: '👈', name: 'Backhand Index Pointing Left', category: 'people' },
        { emoji: '👉', name: 'Backhand Index Pointing Right', category: 'people' },
        { emoji: '👆', name: 'Backhand Index Pointing Up', category: 'people' },
        { emoji: '👇', name: 'Backhand Index Pointing Down', category: 'people' },
        { emoji: '🖐️', name: 'Hand with Fingers Splayed', category: 'people' },
        { emoji: '✋', name: 'Raised Hand', category: 'people' },
        { emoji: '🤚', name: 'Raised Back of Hand', category: 'people' },
        { emoji: '🤟', name: 'Love-You Gesture', category: 'people' },
        { emoji: '👌', name: 'OK Hand', category: 'people' },
        { emoji: '🤘', name: 'Sign of the Horns', category: 'people' },
        { emoji: '🤌', name: 'Pinched Fingers', category: 'people' },
        { emoji: '👨‍👩‍👧‍👦', name: 'Family', category: 'people' },
        { emoji: '🧑‍🚀', name: 'Astronaut', category: 'people' },
        { emoji: '👨‍🎤', name: 'Man Singer', category: 'people' },
        { emoji: '👩‍🎤', name: 'Woman Singer', category: 'people' },

        // Animals category
        { emoji: '🐱', name: 'Cat Face', category: 'animals' },
        { emoji: '🐶', name: 'Dog Face', category: 'animals' },
        { emoji: '🦊', name: 'Fox', category: 'animals' },
        { emoji: '🐼', name: 'Panda', category: 'animals' },
        { emoji: '🦁', name: 'Lion', category: 'animals' },
        { emoji: '🐨', name: 'Koala', category: 'animals' },
        { emoji: '🦄', name: 'Unicorn', category: 'animals' },
        { emoji: '🦋', name: 'Butterfly', category: 'animals' },
        { emoji: '🐢', name: 'Turtle', category: 'animals' },
        { emoji: '🦉', name: 'Owl', category: 'animals' },
        { emoji: '🦖', name: 'T-Rex', category: 'animals' },
        { emoji: '🐙', name: 'Octopus', category: 'animals' },

        // Food category
        { emoji: '🍕', name: 'Pizza', category: 'food' },
        { emoji: '🍰', name: 'Shortcake', category: 'food' },
        { emoji: '🍎', name: 'Red Apple', category: 'food' },
        { emoji: '🍔', name: 'Hamburger', category: 'food' },
        { emoji: '🍦', name: 'Ice Cream', category: 'food' },
        { emoji: '🍩', name: 'Doughnut', category: 'food' },
        { emoji: '🍜', name: 'Steaming Bowl', category: 'food' },
        { emoji: '🥗', name: 'Green Salad', category: 'food' },
        { emoji: '🍣', name: 'Sushi', category: 'food' },
        { emoji: '🌮', name: 'Taco', category: 'food' },
        { emoji: '🍷', name: 'Wine Glass', category: 'food' },
        { emoji: '☕', name: 'Hot Beverage', category: 'food' },

        // Activities category
        { emoji: '⚽', name: 'Soccer Ball', category: 'activities' },
        { emoji: '🎮', name: 'Video Game', category: 'activities' },
        { emoji: '🎨', name: 'Artist Palette', category: 'activities' },
        { emoji: '🎯', name: 'Direct Hit', category: 'activities' },
        { emoji: '🏆', name: 'Trophy', category: 'activities' },
        { emoji: '🎬', name: 'Clapper Board', category: 'activities' },
        { emoji: '🎤', name: 'Microphone', category: 'activities' },
        { emoji: '🎸', name: 'Guitar', category: 'activities' },
        { emoji: '🎭', name: 'Performing Arts', category: 'activities' },
        { emoji: '🧩', name: 'Puzzle Piece', category: 'activities' },
        { emoji: '⛷️', name: 'Skier', category: 'activities' },
        { emoji: '🏄', name: 'Person Surfing', category: 'activities' },

        // Travel category
        { emoji: '✈️', name: 'Airplane', category: 'travel' },
        { emoji: '🏖️', name: 'Beach with Umbrella', category: 'travel' },
        { emoji: '🚗', name: 'Car', category: 'travel' },
        { emoji: '🏔️', name: 'Mountain', category: 'travel' },
        { emoji: '🗺️', name: 'World Map', category: 'travel' },
        { emoji: '🚀', name: 'Rocket', category: 'travel' },
        { emoji: '🚲', name: 'Bicycle', category: 'travel' },
        { emoji: '⛵', name: 'Sailboat', category: 'travel' },
        { emoji: '🚆', name: 'Train', category: 'travel' },
        { emoji: '🏙️', name: 'Cityscape', category: 'travel' },
        { emoji: '🌋', name: 'Volcano', category: 'travel' },
        { emoji: '🏝️', name: 'Desert Island', category: 'travel' },

        // Symbols category
        { emoji: '💡', name: 'Light Bulb', category: 'symbols' },
        { emoji: '💯', name: 'Hundred Points', category: 'symbols' },
        { emoji: '❤️', name: 'Red Heart', category: 'symbols' },
        { emoji: '🔥', name: 'Fire', category: 'symbols' },
        { emoji: '✨', name: 'Sparkles', category: 'symbols' },
        { emoji: '🌟', name: 'Glowing Star', category: 'symbols' },
        { emoji: '⭐', name: 'Star', category: 'symbols' },
        { emoji: '💫', name: 'Dizzy', category: 'symbols' },
        { emoji: '💎', name: 'Gem Stone', category: 'symbols' },
        { emoji: '🔔', name: 'Bell', category: 'symbols' },
        { emoji: '🎵', name: 'Musical Note', category: 'symbols' },
        { emoji: '⚡', name: 'High Voltage', category: 'symbols' },
        { emoji: '🔴', name: 'Red Circle', category: 'symbols' },
        { emoji: '🟠', name: 'Orange Circle', category: 'symbols' },
        { emoji: '🟡', name: 'Yellow Circle', category: 'symbols' },
        { emoji: '🟢', name: 'Green Circle', category: 'symbols' },
        { emoji: '🔵', name: 'Blue Circle', category: 'symbols' },
        { emoji: '🟣', name: 'Purple Circle', category: 'symbols' },
        { emoji: '⚫', name: 'Black Circle', category: 'symbols' },
        { emoji: '⚪', name: 'White Circle', category: 'symbols' },
        { emoji: '♥️', name: 'Heart Suit', category: 'symbols' },
        { emoji: '♦️', name: 'Diamond Suit', category: 'symbols' },
        { emoji: '♣️', name: 'Club Suit', category: 'symbols' },
        { emoji: '♠️', name: 'Spade Suit', category: 'symbols' },
        { emoji: '⏰', name: 'Alarm Clock', category: 'symbols' },
        { emoji: '⏱️', name: 'Stopwatch', category: 'symbols' },
        { emoji: '🧿', name: 'Nazar Amulet', category: 'symbols' },
        { emoji: '☮️', name: 'Peace Symbol', category: 'symbols' },
        { emoji: '☯️', name: 'Yin Yang', category: 'symbols' },
        { emoji: '☢️', name: 'Radioactive', category: 'symbols' },
        { emoji: '☣️', name: 'Biohazard', category: 'symbols' },

        // Objects category
        { emoji: '📱', name: 'Mobile Phone', category: 'objects' },
        { emoji: '💻', name: 'Laptop', category: 'objects' },
        { emoji: '⌚', name: 'Watch', category: 'objects' },
        { emoji: '📷', name: 'Camera', category: 'objects' },
        { emoji: '🔋', name: 'Battery', category: 'objects' },
        { emoji: '💡', name: 'Light Bulb', category: 'objects' },
        { emoji: '🔍', name: 'Magnifying Glass', category: 'objects' },
        { emoji: '🧸', name: 'Teddy Bear', category: 'objects' },
        { emoji: '🎁', name: 'Wrapped Gift', category: 'objects' },
        { emoji: '📚', name: 'Books', category: 'objects' },
        { emoji: '📝', name: 'Memo', category: 'objects' },
        { emoji: '🧮', name: 'Abacus', category: 'objects' },
        { emoji: '🔒', name: 'Locked', category: 'objects' },
        { emoji: '🔑', name: 'Key', category: 'objects' },
        { emoji: '🧲', name: 'Magnet', category: 'objects' },
        { emoji: '💰', name: 'Money Bag', category: 'objects' },
        { emoji: '💳', name: 'Credit Card', category: 'objects' },
        { emoji: '💎', name: 'Gem Stone', category: 'objects' },
        { emoji: '⚓', name: 'Anchor', category: 'objects' },
        { emoji: '⚒️', name: 'Hammer and Pick', category: 'objects' },
        { emoji: '🔨', name: 'Hammer', category: 'objects' },
        { emoji: '🧰', name: 'Toolbox', category: 'objects' },
        { emoji: '🔧', name: 'Wrench', category: 'objects' },
        { emoji: '🧬', name: 'DNA', category: 'objects' },
        { emoji: '🔬', name: 'Microscope', category: 'objects' },
        { emoji: '🔭', name: 'Telescope', category: 'objects' },
        { emoji: '📡', name: 'Satellite Antenna', category: 'objects' },
        { emoji: '💉', name: 'Syringe', category: 'objects' },
        { emoji: '🧪', name: 'Test Tube', category: 'objects' },
        { emoji: '🧫', name: 'Petri Dish', category: 'objects' },
        { emoji: '⚰️', name: 'Coffin', category: 'objects' }
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
    if (!activeChat) return [];

    const chatMessages = messages[activeChat] || [];

    // CRITICAL: Sort messages by timestamp to ensure consistent chronological order
    // This ensures messages are ALWAYS displayed in the exact order they were sent/received
    // regardless of what order they arrived in via websockets or API
    return [...chatMessages].sort((a, b) => {
      // Parse dates consistently to avoid timezone or format issues
      const timeA = new Date(a.timestamp || a.created_at || 0).getTime();
      const timeB = new Date(b.timestamp || b.created_at || 0).getTime();

      // If timestamps are exactly the same (rare), use message ID as secondary sort
      if (timeA === timeB) {
        // Temp IDs always go last if timestamps match
        if (a.id.toString().startsWith('temp-')) return 1;
        if (b.id.toString().startsWith('temp-')) return -1;
        return a.id.localeCompare(b.id);
      }

      return timeA - timeB;
    });
  }, [activeChat, messages]);

  // Handle sending a message
  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !activeChat) return;

    // First check if we're authenticated
    if (!currentUser) {
      console.error("Cannot send message: Not authenticated");
      setNotification({
        message: 'Please log in to send messages',
        type: 'error',
        timeout: 3000
      });
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

    // Send the message with improved error handling
    sendMessage(activeChat, messageToSend)
      .then(response => {
        console.log("Message sent successfully:", response);
      })
      .catch(error => {
        console.error("Error sending message:", error);

        // Show more specific error message based on the response code
        let errorMessage = 'Failed to send message. Please try again.';

        if (error.response) {
          // Server responded with an error
          if (error.response.status === 401) {
            errorMessage = 'You need to be logged in to send messages. Please log in again.';
            // Redirect to login after a short delay
            setTimeout(() => {
              window.location.href = '/login';
            }, 2000);
          } else if (error.response.status === 404) {
            errorMessage = 'Cannot send message. The message service is currently unavailable.';
          } else if (error.response.status === 403) {
            errorMessage = 'You do not have permission to send messages to this user.';
          } else if (error.response.status === 500) {
            errorMessage = 'Server error occurred while sending message. Please try again later.';
          }

          // Use custom error message if provided by server
          if (error.response.data && error.response.data.detail) {
            errorMessage = `Failed to send message: ${error.response.data.detail}`;
          }
        } else if (error.request) {
          // Request was made but no response received (network error)
          errorMessage = 'Network error. Please check your internet connection and try again.';
        }

        // Show notification with the error message
        setNotification({
          message: errorMessage,
          type: 'error',
          timeout: 5000
        });
      });
  };

  // Handle searching for users
  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchTerm(query);

    // If search is cleared, reset results
    if (!query.trim()) {
      return;
    }

    if (query.length >= 2) {
      searchUsers(query);
    }
  };

  // Send contact request handler
  const handleSendContactRequest = async (userId) => {
    try {
      // Fix: Define a local contactRequestError state instead of using setError
      setContactRequestError('');
      // Remove direct setLoading calls and use the proper method from useContacts

      const result = await sendContactRequest(userId);
      if (result && result.success) {
        // Success! No error to set.
        // Maybe show a success toast or message
        setNotification({
          message: 'Contact request sent successfully',
          type: 'success',
          timeout: 3000
        });
      } else if (result && !result.success) {
        setContactRequestError(result.message || 'Failed to send contact request. Please try again.');
      }
    } catch (error) {
      console.error('Error sending contact request:', error);
      setContactRequestError('Failed to send contact request. Please try again.');
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
    if (contacts?.length > 0 && !contactsLoading) {
      initialDataLoadedRef.current = true;
    }
  }, [contacts, contactsLoading]);

  // Add a helper function to determine if contacts data is actually in a loading state
  const isContactsLoading = () => {
    // Consider contacts as loading only if:
    // 1. contactsLoading is true
    // 2. We haven't loaded data yet (initialDataLoadedRef.current is false)
    // 3. We don't have any contacts data yet (contacts.length === 0)
    return contactsLoading && !initialDataLoadedRef.current && contacts.length === 0;
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
      // Fix: Use the correct token key
      const token = localStorage.getItem('token');
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
            console.error("Token has expired or is invalid. User needs to login again.");
            setConnectionError(true);
            clearInterval(tokenVerificationInterval);
          }
        });
    }, 60000); // Check every minute

    // Clean up interval on unmount
    return () => {
      clearInterval(tokenVerificationInterval);
    };
  }, [currentUser, refreshContacts, refreshRequests, refreshSentRequests, refreshNotifications, contacts, logout]);

  // Update the authentication verification useEffect to include missing dependencies
  useEffect(() => {
    if (!activeChat || !currentUser) {
      return;
    }

    // Check for properly authenticated
    const token = localStorage.getItem('token');
    if (!token || !currentUser) {
      console.error("Cannot load messages: Not properly authenticated");
      setConnectionError(true);
      return;
    }

    refreshMessages(activeChat);
  }, [activeChat, currentUser, setConnectionError]);

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
    if (activeChat) {
      console.log(`Loading messages for active chat: ${activeChat}`);
      refreshMessages(activeChat, false); // Not silent, show loading indicator
    }
  }, [activeChat]);

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
      await api.delete('/user');

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

  // Keep only the implementation that uses the WebSocket and onlineStatus state
  // Keep this implementation at the end after all other useEffects:
  // Add state for tracking online status
  const [onlineStatus, setOnlineStatus] = useState({});

  // Setup WebSocket connection for real-time online status
  useEffect(() => {
    console.log("Setting up WebSocket connection for presence tracking");

    // Establish WebSocket connection to backend with proper protocol
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const socket = new WebSocket(`${protocol}//${window.location.hostname}:8000/ws/presence/`);

    socket.onopen = () => {
      console.log("WebSocket connection established for presence tracking");

      // Send current user's online status immediately when connected
      if (currentUser) {
        const statusMessage = JSON.stringify({
          userId: currentUser.id,
          online: true
        });
        console.log("Sending online status:", statusMessage);
        socket.send(statusMessage);
      }
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Received presence update:", data);

        // Update online status based on received data
        if (data.userId && data.hasOwnProperty('online')) {
          console.log(`Setting user ${data.userId} online status to ${data.online}`);
          setOnlineStatus(prevStatus => ({
            ...prevStatus,
            [data.userId]: data.online
          }));
        }
      } catch (error) {
        console.error("Error processing presence data:", error);
      }
    };

    // Set up a ping interval to keep the connection alive
    const pingInterval = setInterval(() => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000); // ping every 30 seconds

    // Clean up WebSocket connection when component unmounts
    return () => {
      clearInterval(pingInterval);

      // Send offline status before closing
      if (socket.readyState === WebSocket.OPEN && currentUser) {
        socket.send(JSON.stringify({
          userId: currentUser.id,
          online: false
        }));
        socket.close();
      }
    };
  }, [currentUser]);

  // Define isUserOnline function (only once) after the useEffect
  const isUserOnline = (userId) => {
    return !!onlineStatus[userId];
  };

  // Add filteredSearchResults using useMemo (after other state declarations)
  const filteredSearchResults = useMemo(() => {
    if (!searchResults || !searchTerm) return searchResults;

    const normalizedSearchTerm = searchTerm.toLowerCase().trim();

    return searchResults.filter(user => {
      const username = (user.username || '').toLowerCase();
      const userId = (user.id || '').toString().toLowerCase();

      return username.includes(normalizedSearchTerm) || userId.includes(normalizedSearchTerm);
    });
  }, [searchResults, searchTerm]);

  // Add a state for tracking unread messages
  const [unreadMessages, setUnreadMessages] = useState(0);

  // Add this useEffect to count unread messages
  useEffect(() => {
    // Only count unread messages if we have messages and they are in an array
    if (messages && Array.isArray(messages)) {
      const count = messages.filter(msg =>
        !msg.read &&
        msg.to_user === currentUser.id &&
        (!activeChat || msg.from_user !== activeChat)
      ).length;

      setUnreadMessages(count);
    } else {
      // If messages is not an array, set count to 0
      setUnreadMessages(0);
    }
  }, [messages, activeChat, currentUser.id]);

  // Add useEffect to scroll to bottom when chat is opened or messages change
  useEffect(() => {
    // Scroll to bottom whenever active chat or messages change
    if (activeChat && messageListRef.current) {
      setTimeout(scrollToBottom, 100); // slight delay to ensure rendering completes
    }
  }, [activeChat, activeChatMessages]);

  // Add a useEffect to scroll to bottom whenever messages change
  useEffect(() => {
    // Only scroll if we have messages and are viewing the active chat
    if (activeChatMessages.length > 0) {
      scrollToBottomRef.current();
    }
  }, [activeChatMessages]);

  // Handle user online status through WebSocket
  useEffect(() => {
    if (!currentUser) return;

    // WebSocket connection is handled in MessagesContext
    // Here we just listen for and process presence updates
    const handleWebSocketMessage = (event) => {
      try {
        // Access data from the CustomEvent's detail property
        const data = event.detail;

        // Handle presence updates
        if (data.type === 'presence') {
          const { userId, online } = data;
          setOnlineStatus(prev => ({
            ...prev,
            [userId]: online
          }));
        }
      } catch (error) {
        console.error('Error processing presence data:', error);
      }
    };

    // Listen for messages from the WebSocket connection in MessagesContext
    window.addEventListener('ws-message', handleWebSocketMessage);

    // Clean up
    return () => {
      window.removeEventListener('ws-message', handleWebSocketMessage);
    };
  }, [currentUser]);

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

      {/* Main content */}
      <header className="dashboard-header">
        <h2>ClearBox</h2>
        <div className="user-controls">
          <div className="notification-badge" onClick={() => setShowNotifications(!showNotifications)}>
            <span className="notification-icon">🔔</span>
            {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
          </div>
          <span className="user-display">{displayName}</span>
          <button onClick={handleLogout} className="button-outline">Logout</button>
        </div>
      </header>

      {/* Notifications dropdown */}
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
              <button onClick={() => setActiveSection('messages')}>
                <span className="nav-text">Messages</span>
                {unreadMessages > 0 && <span className="badge message-badge">{unreadMessages}</span>}
              </button>
            </li>
            <li className={activeSection === 'groups' ? 'active' : ''}>
              <button onClick={() => setActiveSection('groups')}>
                <span className="nav-text">Groups</span>
              </button>
            </li>
            <li className={activeSection === 'contacts' ? 'active' : ''}>
              <button onClick={() => setActiveSection('contacts')}>
                <span className="nav-text">Contacts</span>
                {contactRequests?.length > 0 && <span className="badge contact-badge">{contactRequests.length}</span>}
              </button>
            </li>
            <li className={activeSection === 'profile' ? 'active' : ''}>
              <button onClick={() => setActiveSection('profile')}>
                <span className="nav-text">Profile</span>
              </button>
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
                    <div className="section-actions">
                      <button
                        className="icon-button"
                        title="Search in contacts"
                        onClick={() => {
                          // Create a state for contact search if it doesn't exist yet
                          if (!window.contactSearchVisible) {
                            window.contactSearchVisible = true;
                            // Add a search input to the contacts list
                            const searchInput = document.createElement('input');
                            searchInput.type = 'text';
                            searchInput.placeholder = 'Search contacts...';
                            searchInput.className = 'contact-search-input';
                            searchInput.addEventListener('input', (e) => {
                              const searchTerm = e.target.value.toLowerCase();
                              // Find all contact items
                              const contactItems = document.querySelectorAll('.contact-item');
                              contactItems.forEach(item => {
                                const contactName = item.querySelector('.contact-name').textContent.toLowerCase();
                                if (contactName.includes(searchTerm) || searchTerm === '') {
                                  item.style.display = 'flex';
                                } else {
                                  item.style.display = 'none';
                                }
                              });
                            });

                            // Insert at the top of contacts list
                            const contactsList = document.querySelector('.contacts-list');
                            contactsList.insertBefore(searchInput, contactsList.firstChild);

                            // Focus the input
                            searchInput.focus();
                          } else {
                            // Toggle visibility
                            const searchInput = document.querySelector('.contact-search-input');
                            if (searchInput) {
                              if (searchInput.style.display === 'none') {
                                searchInput.style.display = 'block';
                                searchInput.focus();
                              } else {
                                searchInput.style.display = 'none';
                                // Reset visibility of all contacts
                                const contactItems = document.querySelectorAll('.contact-item');
                                contactItems.forEach(item => {
                                  item.style.display = 'flex';
                                });
                              }
                            }
                          }
                        }}
                      >
                        🔍
                      </button>
                    </div>
                  </div>

                  {/* Contacts list */}
                  <div className="contacts-list">
                    {isContactsLoading() ? (
                      <div className="loading-indicator">Loading contacts...</div>
                    ) : contacts && contacts.length > 0 ? (
                      contacts.map(contact => (
                        <div
                          className={`contact-item ${activeChat === contact.id ? 'active' : ''}`}
                          key={contact.id}
                          onClick={() => setActiveChat(contact.id)}
                        >
                          <UserAvatar username={contact.username} />
                          <div className="contact-info">
                            <span className="contact-name">{contact.username}</span>
                            <span className="contact-status">
                              <span className={`status-dot ${isUserOnline(contact.id) ? 'online' : 'offline'}`}></span>
                              <span className="status-text">{isUserOnline(contact.id) ? 'Online' : 'Offline'}</span>
                            </span>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="no-contacts">
                        <p>No contacts found</p>
                        <button
                          className="search-contacts-btn"
                          onClick={() => {
                            setActiveSection('contacts');
                            setShowSearch(true);
                          }}
                        >
                          Find Contacts
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                <div className="chat-area">
                  {activeChat ? (
                    <>
                      <div className="chat-header">
                        <div className="chat-contact-info">
                          <UserAvatar username={getContactDetails(activeChat)?.username} />
                          <div>
                            <h3 className="contact-name-display">{getContactDetails(activeChat)?.username}</h3>
                            <div className={`status ${isUserOnline(activeChat) ? 'online' : 'offline'}`}>
                              {isUserOnline(activeChat) ? 'Online' : 'Offline'}
                            </div>
                          </div>
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
                                // CRITICAL: Sort by timestamp, oldest first (newer messages at bottom)
                                // This sort is the final safeguard to ensure messages are always displayed chronologically
                                // Messages should already be sorted in MessagesContext but this ensures proper display order
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
                          <div className="empty-chat">
                            <p>No messages yet with {getContactDetails(activeChat)?.username}</p>
                            <button className="start-chat-btn" onClick={() => document.querySelector('.message-form input').focus()}>
                              Start Conversation
                            </button>
                          </div>
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
                                <button
                                  className={`emoji-category ${activeEmojiCategory === 'objects' ? 'active' : ''}`}
                                  onClick={() => setActiveEmojiCategory('objects')}
                                  title="Objects"
                                >
                                  📱
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
                      <p>Select a contact from the list to start a secure conversation</p>
                      {contacts && contacts.length > 0 ? (
                        <button
                          className="search-contacts-btn"
                          onClick={() => {
                            setShowSearch(true);
                            setTimeout(() => document.querySelector('.search-bar input')?.focus(), 100);
                          }}
                        >
                          Find Contacts
                        </button>
                      ) : (
                        <button
                          className="search-contacts-btn"
                          onClick={() => {
                            setShowSearch(true);
                            setTimeout(() => document.querySelector('.search-bar input')?.focus(), 100);
                          }}
                        >
                          Find Contacts
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeSection === 'groups' && (
            <div className="groups-section">
              <GroupChat />
            </div>
          )}

          {activeSection === 'contacts' && (
            <div className="contacts-section">
              <div className="tabs">

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
                    {searchLoading ? (
                      <div className="loading-indicator">Searching...</div>
                    ) : filteredSearchResults && filteredSearchResults.length > 0 ? (
                      <div className="search-results-list">
                        {filteredSearchResults.map(user => (
                          <div className="user-card" key={user.id}>
                            <div className="user-info">
                              <h4>{user.username}</h4>
                              <p>{user.email}</p>
                            </div>
                            <button
                              className="button-small"
                              onClick={() => handleSendContactRequest(user.id)}
                              disabled={false}
                            >
                              Add Contact
                            </button>
                          </div>
                        ))}
                      </div>
                    ) : searchTerm && searchTerm.length >= 2 ? (
                      <div className="no-results">
                        <p>No users found matching "{searchTerm}"</p>
                        <p className="search-tip">Try a different search term or check the spelling.</p>
                      </div>
                    ) : (
                      <div className="search-info">
                        <p>Enter a username or email to search for users</p>
                        <p className="search-tip">Minimum 2 characters required</p>
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
                      {contactRequests && contactRequests.length > 0 ? (
                        contactRequests.map(request => (
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
                        ))
                      ) : (
                        <div className="no-requests-message">
                          <p>You're all caught up! No pending contact requests.</p>
                          <p className="request-tip">Looking to connect? Try finding users in the search tab.</p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="my-contacts-section">
                    <h3>My Contacts</h3>
                    <div className="contacts-grid">
                      {contacts?.length > 0 ? (
                        contacts.map(contact => (
                          <div key={contact.id} className="contact-card">
                            <UserAvatar username={contact.username || 'Unknown'} size="40px" />
                            <div className="contact-info">
                              <div className="username">{contact.username || 'Unknown User'}</div>
                              <div className="status-indicator">
                                <span className={`status-dot ${isUserOnline(contact.id) ? 'online' : 'offline'}`}></span>
                                <span className="status-text">{isUserOnline(contact.id) ? 'Online' : 'Offline'}</span>
                              </div>
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
                        <div className="no-contacts-message">
                          <p>Your contacts list is empty.</p>
                          <p className="contact-tip">Start by finding and adding users in the "Find Users" tab.</p>
                          <button
                            className="find-users-btn"
                            onClick={() => setShowSearch(true)}
                          >
                            Find Users
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}
              </div>
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

// Terms of Service Component
const TermsOfService = () => {
  return (
    <div className="terms-container">
      <div className="terms-content">
        <h1>Terms of Service</h1>
        <p className="last-updated">Last Updated: {new Date().toISOString().slice(0, 10)}</p>

        <section>
          <h2>1. Introduction</h2>
          <p>
            Welcome to ClearBox. By using our platform, you agree to these Terms of Service ("Terms").
            Please read them carefully. If you don't agree with these Terms, you may not use ClearBox.
          </p>
          <p>
            Our service provides end-to-end encrypted messaging and secure communication tools designed with
            privacy and security as the foundation. These Terms govern your use of ClearBox and form a legal
            agreement between you and ClearBox.
          </p>
        </section>

        <section>
          <h2>2. Definitions</h2>
          <p>Throughout these Terms, we use certain terms with specific meanings:</p>
          <ul>
            <li><strong>"ClearBox"</strong> refers to our platform, services, and company.</li>
            <li><strong>"User"</strong> means any person who creates an account and uses ClearBox.</li>
            <li><strong>"Content"</strong> means any messages, data, information, text, graphics, or other materials uploaded, downloaded, or appearing on ClearBox.</li>
            <li><strong>"Personal Data"</strong> means information relating to an identified or identifiable natural person.</li>
          </ul>
        </section>

        <section>
          <h2>3. Account Registration and Eligibility</h2>
          <p>
            To use ClearBox, you must register for an account. You agree to provide accurate, current, and complete
            information during registration and to update your information to keep it accurate, current, and complete.
          </p>
          <p>
            You must be at least 16 years old to use ClearBox. By using ClearBox, you represent that you meet this
            age requirement.
          </p>
          <p>
            You are responsible for maintaining the confidentiality of your account credentials and for all
            activities that occur under your account. You agree to notify us immediately of any unauthorized
            use of your account.
          </p>
        </section>

        <section>
          <h2>4. Privacy and Data Protection</h2>
          <p>
            ClearBox is committed to protecting your privacy. Our <Link to="/privacy-policy">Privacy Policy</Link> explains
            our data collection, use, and storage practices. By using ClearBox, you agree to the
            collection and use of information as detailed in our Privacy Policy.
          </p>
          <p>
            We comply with the General Data Protection Regulation (GDPR) and other applicable privacy laws.
            As a user, you have specific rights regarding your personal data, as outlined in our Privacy Policy.
          </p>
        </section>

        <section>
          <h2>5. Service Usage Rules</h2>
          <p>When using ClearBox, you agree not to:</p>
          <ul>
            <li>Violate any applicable laws or regulations.</li>
            <li>Infringe on the rights of others, including intellectual property rights.</li>
            <li>Share harmful, illegal, or objectionable content.</li>
            <li>Attempt to bypass ClearBox's security features or encryption protocols.</li>
            <li>Use ClearBox to send spam, unsolicited messages, or harass other users.</li>
            <li>Attempt to interfere with, compromise, or harm the ClearBox platform or servers.</li>
            <li>Create multiple accounts for deceptive or malicious purposes.</li>
            <li>Impersonate another person or misrepresent your affiliation with any person or entity.</li>
          </ul>
          <p>
            We reserve the right to remove any content or suspend any account that violates these rules.
          </p>
        </section>

        <section>
          <h2>6. Intellectual Property Rights</h2>
          <p>
            ClearBox and its original content, features, and functionality are owned by ClearBox and
            are protected by international copyright, trademark, patent, trade secret, and other intellectual
            property or proprietary rights laws.
          </p>
          <p>
            You retain ownership of any content you share through ClearBox. However, by using our services,
            you grant us a limited license to store and transmit your content solely for the purpose of
            providing and improving our services.
          </p>
        </section>

        <section>
          <h2>7. Termination</h2>
          <p>
            You can terminate your account at any time through the platform's "Delete Account" feature.
          </p>
          <p>
            We reserve the right to suspend or terminate your account and access to ClearBox at our sole
            discretion, without notice, for conduct that we believe violates these Terms or is harmful
            to other users, us, or third parties, or for any other reason.
          </p>
          <p>
            Upon termination, your right to use ClearBox will immediately cease. All provisions of these
            Terms which by their nature should survive termination shall survive, including ownership
            provisions, warranty disclaimers, indemnity, and limitations of liability.
          </p>
        </section>

        <section>
          <h2>8. Disclaimer of Warranties</h2>
          <p>
            ClearBox is provided "as is" and "as available" without any warranties of any kind, either
            express or implied, including but not limited to the implied warranties of merchantability,
            fitness for a particular purpose, or non-infringement.
          </p>
          <p>
            We do not guarantee that ClearBox will be uninterrupted, timely, secure, or error-free.
            While we strive to provide a secure platform with end-to-end encryption, no digital
            communication method is 100% secure, and we cannot guarantee absolute security.
          </p>
        </section>

        <section>
          <h2>9. Limitation of Liability</h2>
          <p>
            To the maximum extent permitted by law, in no event shall ClearBox be liable for any indirect,
            incidental, special, consequential, or punitive damages, or any loss of profits or revenues,
            whether incurred directly or indirectly, or any loss of data, use, goodwill, or other intangible
            losses resulting from your access to or use of or inability to access or use ClearBox.
          </p>
          <p>
            Our liability is limited to the maximum extent permitted by law, and in cases where limitation
            is not permitted, our liability shall be limited to the fullest extent allowed.
          </p>
        </section>

        <section>
          <h2>10. Changes to Terms</h2>
          <p>
            We may modify these Terms at any time. We will notify you of significant changes by posting
            a notice on our platform or sending you an email. Your continued use of ClearBox after changes
            become effective constitutes your acceptance of the updated Terms.
          </p>
          <p>
            It is your responsibility to review these Terms periodically. The "Last Updated" date at the
            top of this page indicates when these Terms were last revised.
          </p>
        </section>

        <section>
          <h2>11. Governing Law</h2>
          <p>
            These Terms shall be governed by and construed in accordance with the laws of Finland,
            without regard to its conflict of laws principles.
          </p>
          <p>
            Any disputes arising under or in connection with these Terms shall be subject to the exclusive
            jurisdiction of the courts in Finland.
          </p>
        </section>

        <section>
          <h2>12. Contact Information</h2>
          <p>
            If you have any questions about these Terms, please contact us at:
            <br />
            Email: <a href="mailto:contact@clearbox.live">contact@clearbox.live</a>
          </p>
        </section>

        <div className="terms-footer">
          <Link to="/login" className="button">Return to Login</Link>
          <Link to="/" className="button-outline">Back to Home</Link>
        </div>
      </div>
    </div>
  );
};

// About Me Component
const About = () => {
  return (
    <div className="about-container">
      <header className="about-header">
        <div className="container">
          <Link to="/" className="back-link">
            <span className="back-icon">←</span> Back to Home
          </Link>
          <h1>About the Creator</h1>
        </div>
      </header>

      <section className="about-hero">
        <div className="container">
          <div className="about-profile">
            <div className="profile-image-container">
              <div className="profile-image">
                <span className="profile-initial">I</span>
              </div>
            </div>
            <div className="profile-details">
              <h2>Imad Eddine El Mouss</h2>
              <p className="profile-title">Data Engineering & AI Student | Cybersecurity Enthusiast</p>
              <div className="profile-location">
                <span className="location-icon">📍</span> Turku, Finland
              </div>
              <div className="contact-links">
                <a href="mailto:imadeddine200507@gmail.com" className="contact-link">
                  <span className="contact-icon">✉️</span> imadeddine200507@gmail.com
                </a>
                <a href="https://www.linkedin.com/in/imad-eddine-el-mouss-986741262" target="_blank" rel="noopener noreferrer" className="contact-link">
                  <span className="contact-icon">🔗</span> LinkedIn
                </a>
                <a href="https://github.com/imaddde867" target="_blank" rel="noopener noreferrer" className="contact-link">
                  <span className="contact-icon">💻</span> GitHub
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="about-content">
        <div className="container">
          <div className="about-intro">
            <h3>Meet the Mind Behind ClearBox</h3>
            <p>
              Hello! I'm Imad, a motivated Data Engineering & AI student passionate about building scalable,
              secure, and privacy-focused applications. ClearBox was born from my commitment to creating
              communication systems that respect user privacy while delivering a seamless experience.
            </p>
            <p>
              With a background in data engineering and a focus on security, I've designed ClearBox to
              demonstrate how modern applications can be both user-friendly and compliant with the highest
              privacy standards like GDPR.
            </p>
          </div>

          <div className="about-expertise">
            <h3>Technical Expertise</h3>
            <div className="expertise-grid">
              <div className="expertise-category">
                <h4>Software & Data Engineering</h4>
                <ul className="skills-list">
                  <li><span className="skill-tag">Python (Advanced)</span></li>
                  <li><span className="skill-tag">Apache Airflow</span></li>
                  <li><span className="skill-tag">Apache Spark</span></li>
                  <li><span className="skill-tag">PySpark</span></li>
                  <li><span className="skill-tag">REST APIs</span></li>
                  <li><span className="skill-tag">Django</span></li>
                  <li><span className="skill-tag">Flask</span></li>
                </ul>
              </div>

              <div className="expertise-category">
                <h4>Real-Time Systems</h4>
                <ul className="skills-list">
                  <li><span className="skill-tag">Apache Pulsar</span></li>
                  <li><span className="skill-tag">RabbitMQ</span></li>
                  <li><span className="skill-tag">MQTT</span></li>
                  <li><span className="skill-tag">InfluxDB</span></li>
                </ul>
              </div>

              <div className="expertise-category">
                <h4>Databases & Cloud</h4>
                <ul className="skills-list">
                  <li><span className="skill-tag">PostgreSQL</span></li>
                  <li><span className="skill-tag">PostGIS</span></li>
                  <li><span className="skill-tag">Citus</span></li>
                  <li><span className="skill-tag">SQL</span></li>
                  <li><span className="skill-tag">MongoDB</span></li>
                  <li><span className="skill-tag">Amazon S3</span></li>
                  <li><span className="skill-tag">AWS</span></li>
                </ul>
              </div>

              <div className="expertise-category">
                <h4>AI/ML & Analytics</h4>
                <ul className="skills-list">
                  <li><span className="skill-tag">TensorFlow</span></li>
                  <li><span className="skill-tag">Scikit-learn</span></li>
                  <li><span className="skill-tag">Pandas</span></li>
                  <li><span className="skill-tag">Grafana</span></li>
                </ul>
              </div>

              <div className="expertise-category">
                <h4>DevOps</h4>
                <ul className="skills-list">
                  <li><span className="skill-tag">Docker</span></li>
                  <li><span className="skill-tag">Git</span></li>
                  <li><span className="skill-tag">Conda</span></li>
                </ul>
              </div>
            </div>
          </div>

          <div className="about-projects">
            <h3>Featured Projects</h3>

            <div className="project-cards">
              <div className="project-card">
                <div className="project-icon">🚢</div>
                <h4>Maritime Vessel Tracking System</h4>
                <p>
                  Engineered a real-time pipeline processing 10,000+ vessel positions daily, achieving 90% ML-based
                  trajectory accuracy. Optimized algorithms to slash processing time, ideal for transportation solutions.
                </p>
              </div>

              <div className="project-card">
                <div className="project-icon">🎵</div>
                <h4>Spotify Recommendation Engine</h4>
                <p>
                  Designing a scalable ETL pipeline with Apache Spark, targeting 85% ML accuracy on Databricks.
                  Leveraging MongoDB and S3 for efficient data retrieval in large-scale applications.
                </p>
                <div className="project-status">In Progress</div>
              </div>

              <div className="project-card featured">
                <div className="project-icon">💬</div>
                <h4>ClearBox: GDPR-Compliant Messaging</h4>
                <p>
                  Created a secure full on cloud system for 1,000 daily users with end-to-end encryption
                  (100% GDPR compliant). Reduced message latency via optimized queue management.
                </p>
                <div className="project-badge">You are here</div>
              </div>
            </div>
          </div>

          <div className="about-education">
            <h3>Education</h3>
            <div className="education-card">
              <div className="education-icon">🎓</div>
              <div className="education-details">
                <h4>Bachelor of Engineering in Information and Communication Technologies</h4>
                <p className="education-institution">Turku University of Applied Sciences</p>
                <p className="education-period">2023 - Present</p>
                <p className="education-focus">
                  <strong>Specialization:</strong> Data Engineering and Artificial Intelligence<br />
                  <strong>Focus:</strong> Real-time data systems and scalable software solutions for networked societies
                </p>
                <p className="education-courses">
                  <strong>Relevant coursework:</strong> Big Data Engineering, Data Analytics & ML,
                  Cloud Services, Software Development Operations
                </p>
              </div>
            </div>
          </div>

          <div className="about-certifications">
            <h3>Certifications & Languages</h3>
            <div className="certifications-list">
              <div className="certification-group">
                <h4>AWS Academy</h4>
                <ul>
                  <li>Cloud Foundations</li>
                  <li>Machine Learning Foundations</li>
                  <li>Machine Learning for Natural Language Processing</li>
                </ul>
              </div>
              <div className="certification-group">
                <h4>MATLAB</h4>
                <ul>
                  <li>Onramp - MATLAB Fundamentals</li>
                </ul>
              </div>
              <div className="certification-group">
                <h4>Languages</h4>
                <ul>
                  <li><strong>Professional:</strong> English, French, Arabic</li>
                  <li><strong>Conversational (A2):</strong> Finnish</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="about-contact">
        <div className="container">
          <h3>Let's Connect</h3>
          <p>
            I'm always open to discussing technology, data engineering, AI projects, or potential collaborations.
            Feel free to reach out through any of the platforms below:
          </p>
          <div className="contact-methods">
            <a href="mailto:imadeddine200507@gmail.com" className="contact-method">
              <span className="contact-method-icon">✉️</span>
              <span className="contact-method-label">Email</span>
            </a>
            <a href="https://www.linkedin.com/in/imad-eddine-el-mouss-986741262" target="_blank" rel="noopener noreferrer" className="contact-method">
              <span className="contact-method-icon">🔗</span>
              <span className="contact-method-label">LinkedIn</span>
            </a>
            <a href="https://github.com/imaddde867" target="_blank" rel="noopener noreferrer" className="contact-method">
              <span className="contact-method-icon">💻</span>
              <span className="contact-method-label">GitHub</span>
            </a>
          </div>
        </div>
      </section>

      <footer className="about-footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} Imad Eddine El Mouss. All rights reserved.</p>
          <div className="footer-links">
            <Link to="/">Home</Link>
            <Link to="/privacy-policy">Privacy Policy</Link>
            <Link to="/terms">Terms of Service</Link>
          </div>
        </div>
      </footer>
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
          <Route path="/terms" element={<TermsOfService />} />
          <Route path="/about" element={<About />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;