import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './contact.css';

const Contact = () => {
  const [formState, setFormState] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);
  const navigate = useNavigate();

  // Form validation
  const validateForm = () => {
    const newErrors = {};
    
    // Name validation
    if (!formState.name.trim()) {
      newErrors.name = 'Name is required';
    } else if (formState.name.trim().length < 2) {
      newErrors.name = 'Name must be at least 2 characters';
    }
    
    // Email validation
    if (!formState.email.trim()) {
      newErrors.email = 'Email is required';
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formState.email)) {
        newErrors.email = 'Please enter a valid email address';
      }
    }
    
    // Subject validation
    if (!formState.subject.trim()) {
      newErrors.subject = 'Subject is required';
    } else if (formState.subject.trim().length < 3) {
      newErrors.subject = 'Subject must be at least 3 characters';
    }
    
    // Message validation
    if (!formState.message.trim()) {
      newErrors.message = 'Message is required';
    } else if (formState.message.trim().length < 10) {
      newErrors.message = 'Message must be at least 10 characters';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormState(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: null
      }));
    }
  };

  // Sanitize input to prevent XSS
  const sanitizeInput = (input) => {
    return input
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    // Sanitize all inputs
    const sanitizedData = {
      name: sanitizeInput(formState.name),
      email: sanitizeInput(formState.email),
      subject: sanitizeInput(formState.subject),
      message: sanitizeInput(formState.message),
    };
    
    try {
      // In a real application, this would be an API call
      // For demo purposes, we'll simulate a successful submission
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Create email body (this would normally be done server-side)
      const emailBody = `
        Name: ${sanitizedData.name}
        Email: ${sanitizedData.email}
        Subject: ${sanitizedData.subject}
        
        Message:
        ${sanitizedData.message}
      `;
      
      console.log('Email would be sent to imadeddine200507@gmail.com with body:', emailBody);
      
      // Set success status
      setSubmitStatus('success');
      
      // Reset form after success
      setFormState({
        name: '',
        email: '',
        subject: '',
        message: ''
      });
      
      // Redirect user after 3 seconds
      setTimeout(() => {
        navigate('/');
      }, 3000);
      
    } catch (error) {
      console.error('Error submitting form:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Reset status when unmounting
  useEffect(() => {
    return () => {
      setSubmitStatus(null);
    };
  }, []);

  return (
    <div className="contact-page-container">
      <header className="contact-header">
        <div className="container">
          <div className="logo">
            <h1>ClearBox</h1>
            <span className="logo-icon">🔒</span>
          </div>
          <div className="header-nav">
            <Link to="/" className="back-link">
              <span className="back-icon">←</span> Back to Home
            </Link>
          </div>
        </div>
      </header>

      <main className="contact-main">
        <div className="container">
          <div className="contact-content">
            <div className="contact-intro">
              <h1>Contact Us</h1>
              <p>Have a question or want to get in touch? Fill out the form below and we'll get back to you as soon as possible.</p>
            </div>

            <div className="contact-form-container">
              {submitStatus === 'success' ? (
                <div className="form-success-message">
                  <div className="success-icon">✅</div>
                  <h3>Message Sent Successfully!</h3>
                  <p>Thank you for reaching out. We will get back to you shortly.</p>
                  <p>Redirecting you to the homepage...</p>
                </div>
              ) : submitStatus === 'error' ? (
                <div className="form-error-message">
                  <div className="error-icon">❌</div>
                  <h3>Something Went Wrong</h3>
                  <p>We couldn't send your message. Please try again later or contact us directly at <a href="mailto:imadeddine200507@gmail.com">imadeddine200507@gmail.com</a>.</p>
                  <button 
                    className="retry-button"
                    onClick={() => setSubmitStatus(null)}
                  >
                    Try Again
                  </button>
                </div>
              ) : (
                <form className="contact-form" onSubmit={handleSubmit}>
                  <div className="form-group">
                    <label htmlFor="name">Name</label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={formState.name}
                      onChange={handleChange}
                      placeholder="Your name"
                      disabled={isSubmitting}
                      className={errors.name ? 'error' : ''}
                    />
                    {errors.name && <div className="error-text">{errors.name}</div>}
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formState.email}
                      onChange={handleChange}
                      placeholder="Your email address"
                      disabled={isSubmitting}
                      className={errors.email ? 'error' : ''}
                    />
                    {errors.email && <div className="error-text">{errors.email}</div>}
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="subject">Subject</label>
                    <input
                      type="text"
                      id="subject"
                      name="subject"
                      value={formState.subject}
                      onChange={handleChange}
                      placeholder="Message subject"
                      disabled={isSubmitting}
                      className={errors.subject ? 'error' : ''}
                    />
                    {errors.subject && <div className="error-text">{errors.subject}</div>}
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="message">Message</label>
                    <textarea
                      id="message"
                      name="message"
                      value={formState.message}
                      onChange={handleChange}
                      placeholder="Your message"
                      rows="6"
                      disabled={isSubmitting}
                      className={errors.message ? 'error' : ''}
                    ></textarea>
                    {errors.message && <div className="error-text">{errors.message}</div>}
                  </div>
                  
                  <div className="form-actions">
                    <button 
                      type="submit" 
                      className={`submit-button ${isSubmitting ? 'loading' : ''}`}
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? 'Sending...' : 'Send Message'}
                    </button>
                  </div>
                </form>
              )}
            </div>

          </div>
        </div>
      </main>

      <footer className="contact-footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} ClearBox. All rights reserved.</p>
          <div className="footer-links">
            <Link to="/">Home</Link>
            <Link to="/privacy-policy">Privacy Policy</Link>
            <Link to="/terms">Terms of Service</Link>
            <Link to="/about">About</Link>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Contact; 