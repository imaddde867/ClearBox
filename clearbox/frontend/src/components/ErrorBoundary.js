import React, { Component } from 'react';
import './ErrorBoundary.css';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false,
      error: null,
      errorInfo: null,
      errorCount: 0,
      lastError: null
    };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Capture error details for logging
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
    
    // Update state with error details
    this.setState(prevState => {
      const isSameError = prevState.lastError && 
        prevState.lastError.message === error.message;
      
      return {
        error,
        errorInfo,
        // If it's the same error, increment count, otherwise reset
        errorCount: isSameError ? prevState.errorCount + 1 : 1,
        lastError: error
      };
    });
    
    // Report error to monitoring service if available
    if (window.errorReporter) {
      window.errorReporter.captureException(error, { 
        extra: { 
          componentStack: errorInfo.componentStack,
          count: this.state.errorCount
        }
      });
    }
  }
  
  // Reset error state to try recovery
  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null
    });
  }
  
  // Clear local storage in case corrupted data is causing issues
  handleClearData = () => {
    try {
      localStorage.clear();
      console.log('Local storage cleared');
      
      // Reloading the page after clearing storage
      window.location.reload();
    } catch (err) {
      console.error('Failed to clear local storage:', err);
      alert('Could not clear local data. Please try reloading the page.');
    }
  }

  render() {
    const { hasError, error, errorCount } = this.state;
    const { fallback, children } = this.props;
    
    // If a custom fallback is provided, use it
    if (hasError && fallback) {
      return typeof fallback === 'function' 
        ? fallback(error, this.handleReset) 
        : fallback;
    }
    
    // Default error UI
    if (hasError) {
      // For repeated errors, show more aggressive recovery options
      const isRecurringError = errorCount > 1;
      
      return (
        <div className="error-boundary">
          <div className="error-container">
            <h2>Something went wrong</h2>
            <p className="error-message">
              {error ? error.message : 'An unexpected error occurred'}
            </p>
            <div className="error-actions">
              <button 
                className="error-retry" 
                onClick={this.handleReset}
              >
                Try Again
              </button>
              
              {isRecurringError && (
                <button 
                  className="error-clear-data" 
                  onClick={this.handleClearData}
                >
                  Reset App Data
                </button>
              )}
              
              <button 
                className="error-reload" 
                onClick={() => window.location.reload()}
              >
                Reload Page
              </button>
            </div>
            
            {isRecurringError && (
              <p className="recurring-error-notice">
                This error has occurred {errorCount} times. You may need to reset the application data.
              </p>
            )}
          </div>
        </div>
      );
    }

    return children;
  }
}

export default ErrorBoundary; 