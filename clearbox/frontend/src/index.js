import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { AuthProvider } from './contexts/AuthContext';
import { ContactsProvider } from './contexts/ContactsContext';
import { MessagesProvider } from './contexts/MessagesContext';
import { NotificationsProvider } from './contexts/NotificationsContext';
import { GroupsProvider } from './contexts/GroupsContext';
import { testApiConnection } from './utils/testApi';

// Make test function available for debugging
window.testApiConnection = testApiConnection;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider>
      <NotificationsProvider>
        <ContactsProvider>
          <GroupsProvider>
            <MessagesProvider>
              <App />
            </MessagesProvider>
          </GroupsProvider>
        </ContactsProvider>
      </NotificationsProvider>
    </AuthProvider>
  </React.StrictMode>
);