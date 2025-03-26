# ClearBox - Secure Messaging App 🔐

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![React](https://img.shields.io/badge/React-18.x-61DAFB.svg)
![MQTT](https://img.shields.io/badge/MQTT-5.x-orange.svg)

ClearBox is a secure, scalable, GDPR-compliant messaging app built with Python (FastAPI) and React. It features real-time messaging using MQTT, end-to-end encryption, and a modern dark-themed UI.

<p align="center">
  <img src="frontend/logo/vector/default-monochrome-white.svg" alt="ClearBox Logo" width="500"/>
</p>

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture Overview](#-architecture-overview)
- [Code Optimization](#-code-optimization)
- [Technologies Used](#-technologies-used)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Development Process](#-development-process)
- [Testing Strategy](#-testing-strategy)
- [API Endpoints](#-api-endpoints)
- [Technical Implementation Details](#-technical-implementation-details)
- [Troubleshooting](#-troubleshooting)
- [Security Considerations](#-security-considerations)
- [GDPR Compliance](#-gdpr-compliance)
- [Production Deployment](#-production-deployment)
- [Scalability](#-scalability)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **🔒 Secure Authentication**: User registration and JWT-based authentication
- **👥 Contact Management**: Search for users, send/accept contact requests
- **💬 Real-time Messaging**: One-on-one chats and group conversations
- **🛡️ End-to-End Encryption**: Messages are encrypted using Python's cryptography library
- **🔔 Notifications**: Real-time notifications for new messages and contact requests
- **📜 GDPR Compliance**: Users can delete their accounts and data
- **🎨 Modern UI**: Futuristic, dark-themed interface built with React
- **📴 Offline Support**: Message queue for sending messages when offline
- **✓ Read Receipts**: Know when your messages have been delivered and read

---

## 🏗️ Architecture Overview

ClearBox follows a modern client-server architecture with real-time communication:

### Backend Architecture

<details>
<summary>Click to expand backend architecture details</summary>

The backend is built using FastAPI and follows a modular architecture:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # Main application entry point
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy ORM models
│   ├── schemas.py         # Pydantic schemas for validation
│   ├── security.py        # JWT authentication and security
│   ├── encryption.py      # E2E encryption implementation
│   ├── mqtt_client.py     # MQTT client for real-time messaging
│   └── routes/            # API route definitions
│       ├── auth.py        # Authentication endpoints
│       ├── users.py       # User management endpoints
│       ├── contacts.py    # Contact management endpoints
│       ├── messages.py    # Messaging endpoints
│       ├── groups.py      # Group chat endpoints
│       ├── notifications.py # Notification endpoints
│       └── websockets.py  # WebSocket connection handling
├── run.py                 # Server startup script
├── requirements.txt       # Python dependencies
└── .env                   # Environment configuration
```
</details>

### Frontend Architecture

<details>
<summary>Click to expand frontend architecture details</summary>

The React frontend follows a modular component-based architecture:

```
frontend/
├── public/                # Static files
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── ChatWindow/
│   │   ├── ContactList/
│   │   ├── MessageBubble/
│   │   ├── GroupChat/
│   │   └── ...
│   ├── contexts/          # React contexts for state management
│   │   ├── AuthContext.js
│   │   ├── ChatContext.js
│   │   └── ...
│   ├── pages/             # Application pages
│   │   ├── Login/
│   │   ├── Register/
│   │   ├── Dashboard/
│   │   └── ...
│   ├── services/          # API service integrations
│   │   ├── api.js
│   │   ├── mqtt.js
│   │   └── encryption.js
│   ├── utils/             # Utility functions
│   │   ├── validators.js
│   │   └── formatters.js
│   ├── styles/            # CSS and styling
│   ├── App.js             # Main application component
│   └── index.js           # Application entry point
├── package.json           # Node.js dependencies
└── fix_css.js             # CSS optimization script
```
</details>

### Data Flow

<details>
<summary>Click to expand data flow details</summary>

1. **Authentication Flow**:
   - User credentials are validated and a JWT token is issued
   - Token is stored in local storage and included in all API requests
   - Token refresh mechanism extends sessions securely

2. **Messaging Flow**:
   - Messages are encrypted client-side before sending
   - Messages are sent to the server via API endpoints
   - Server broadcasts messages via MQTT to relevant recipients
   - Recipients decrypt messages client-side

3. **Real-time Updates**:
   - MQTT topics follow the pattern: `user/{user_id}/messages`
   - Clients subscribe to their personal topics and group topics
   - Message delivery confirmations are sent back via MQTT
</details>

---

## 🚀 Code Optimization

The codebase has been optimized for better performance and maintainability:

- ✅ Removed unnecessary temporary and backup files
- ✅ Cleaned up Python cache directories and compiled .pyc files
- ✅ Removed trailing whitespace and fixed indentation
- ✅ Ensured consistent coding style throughout the project
- ✅ Removed redundant blank lines while preserving logical separation
- ✅ Optimized imports and dependencies
- ✅ Implemented efficient database queries with proper indexing
- ✅ Added caching for frequently accessed data
- ✅ Optimized React rendering with proper use of memoization

---

## 🛠️ Technologies Used

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core programming language |
| FastAPI | 0.104.0 | High-performance web framework |
| SQLAlchemy | 2.0.22 | ORM for database interactions |
| Pydantic | 2.4.2 | Data validation and settings management |
| PostgreSQL/SQLite | Latest | Primary/Development database |
| JWT | via python-jose 3.3.0 | Token-based authentication |
| Bcrypt | 4.0.1 | Password hashing |
| Cryptography | 41.0.4 | End-to-end encryption library |
| MQTT (Mosquitto) | Latest | Message broker for real-time communication |
| Paho-MQTT | 2.1.0 | MQTT client library for Python |
| Uvicorn | 0.23.2 | ASGI server |

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI library |
| React Router | 6.16.0 | Client-side routing |
| Axios | 1.8.4 | HTTP client for API requests |
| MQTT.js | 5.0.5 | MQTT client for browser |
| FontAwesome | 6.4.2 | Icon library |
| Emoji-picker-react | 4.12.2 | Emoji selector component |
| CSS3 | Latest | Custom styling with advanced animations |
| LocalStorage/SessionStorage | Browser API | Client-side data persistence |

### Development Tools

- **Git**: Version control
- **ESLint**: JavaScript linting
- **Prettier**: Code formatting
- **React DevTools**: React debugging
- **FastAPI Swagger UI**: API documentation and testing

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Node.js 14 or higher
- PostgreSQL (or SQLite for development)
- Mosquitto MQTT Broker

---

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/imaddde867/clearbox.git
cd clearbox
```

### 2. Set Up the Backend

<details>
<summary>Expand backend setup instructions</summary>

#### Create a Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory based on the `.env.example` file:

```ini
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost/clearbox
# For SQLite (development)
# DATABASE_URL=sqlite:///./clearbox.db

# JWT Authentication
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Encryption
ENCRYPTION_KEY=your_encryption_key_here

# MQTT Configuration
MQTT_BROKER=localhost
MQTT_PORT=1883

# Server Configuration
PORT=8001
```

Make sure to replace the placeholders with your actual values.

#### Create the Database

For PostgreSQL:
```sql
CREATE DATABASE clearbox;
```

For SQLite, the database file will be created automatically.

The application will automatically create all the necessary tables when started.
</details>

### 3. Set Up the MQTT Broker (Mosquitto)

<details>
<summary>Expand MQTT setup instructions</summary>

#### Install Mosquitto

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

**macOS:**
```bash
brew install mosquitto
```

**Windows:**
Download the installer from [https://mosquitto.org/download/](https://mosquitto.org/download/)

#### Configure Mosquitto

Create a basic configuration file (mosquitto.conf):

```ini
listener 1883
allow_anonymous true
```

For production, set up proper authentication and TLS:

```ini
listener 1883
allow_anonymous false
password_file /path/to/passwd
cafile /path/to/ca.crt
certfile /path/to/server.crt
keyfile /path/to/server.key
require_certificate true
```
</details>

### 4. Set Up the Frontend

```bash
cd ../frontend
npm install
```

---

## 🚦 Running the Application

### 1. Start the Backend

```bash
cd backend
python run.py --reload
```

The API will be available at http://localhost:8001.  
API documentation is available at http://localhost:8001/docs.

### 2. Start the Frontend

```bash
cd frontend
npm start
```

The frontend will be available at http://localhost:3000.

---

## 📈 Development Process

ClearBox was developed following a feature-driven development approach:

<details>
<summary>Expand development process details</summary>

### Phase 1: Foundation

1. **Project Setup**:
   - Set up FastAPI backend with SQLAlchemy ORM
   - Create React frontend with essential components
   - Configure development environment

2. **Core Authentication**:
   - Implement user registration and login
   - Set up JWT token-based authentication
   - Create secure password hashing

3. **Database Design**:
   - Design normalized database schema
   - Implement database models
   - Set up migrations

### Phase 2: Core Features

1. **Contact Management**:
   - User search functionality
   - Contact request system
   - Contact list management

2. **Basic Messaging**:
   - One-on-one messaging
   - Message storage and retrieval
   - Message history

3. **UI Implementation**:
   - Dark-themed UI design
   - Responsive layout
   - Navigation system

### Phase 3: Advanced Features

1. **Real-time Communication**:
   - MQTT integration
   - Real-time message delivery
   - Online status indicators

2. **End-to-End Encryption**:
   - Encryption key management
   - Message encryption/decryption
   - Secure key exchange

3. **Group Conversations**:
   - Group creation and management
   - Group messaging
   - Member permissions

### Phase 4: Polish and Optimization

1. **Performance Optimization**:
   - Code refactoring
   - Query optimization
   - Caching implementation

2. **UX Enhancements**:
   - Animations and transitions
   - Keyboard shortcuts
   - Usability improvements

3. **GDPR Compliance**:
   - Account deletion
   - Data export
   - Privacy policy implementation
</details>

---

## 🧪 Testing Strategy

ClearBox includes several levels of testing:

<details>
<summary>Expand testing details</summary>

### Unit Tests

- Backend unit tests using pytest
- Frontend component tests using Jest and React Testing Library

### Integration Tests

- API integration tests with pytest
- Frontend integration tests with Cypress

### End-to-End Tests

- Full application flow tests with Cypress
- Authentication flow tests
- Messaging flow tests
</details>

---

## 🔌 API Endpoints

<details>
<summary>Authentication Endpoints</summary>

- `POST /api/signup`: Register a new user
  - Request: `{ "username": "user1", "email": "user1@example.com", "password": "securepassword" }`
  - Response: `{ "id": 1, "username": "user1", "email": "user1@example.com" }`

- `POST /api/login`: Get an access token
  - Request: `{ "username": "user1", "password": "securepassword" }`
  - Response: `{ "access_token": "eyJhbGc...", "token_type": "bearer" }`

- `GET /api/profile`: Get the current user's profile
  - Response: `{ "id": 1, "username": "user1", "email": "user1@example.com", "created_at": "2023-01-01T12:00:00" }`

- `DELETE /api/user`: Delete the current user's account
  - Response: `{ "message": "User account deleted successfully" }`
</details>

<details>
<summary>Contacts Endpoints</summary>

- `GET /api/search?query={query}`: Search for users
  - Response: `[ { "id": 2, "username": "user2" }, ... ]`

- `POST /api/contact/request`: Send a contact request
  - Request: `{ "recipient_id": 2 }`
  - Response: `{ "id": 1, "sender_id": 1, "recipient_id": 2, "status": "pending" }`

- `GET /api/contact/requests`: Get pending contact requests
  - Response: `[ { "id": 1, "sender": { "id": 3, "username": "user3" }, "created_at": "2023-01-01T12:00:00" }, ... ]`

- `POST /api/contact/accept/{request_id}`: Accept a contact request
  - Response: `{ "message": "Contact request accepted" }`

- `POST /api/contact/deny/{request_id}`: Deny a contact request
  - Response: `{ "message": "Contact request denied" }`

- `GET /api/contacts`: Get all contacts
  - Response: `[ { "id": 2, "username": "user2", "online": true, "last_seen": "2023-01-01T12:00:00" }, ... ]`
</details>

<details>
<summary>Messages Endpoints</summary>

- `POST /api/messages`: Send a message (to user or group)
  - Request: `{ "recipient_id": 2, "content": "Hello!", "is_group": false }`
  - Response: `{ "id": 1, "sender_id": 1, "recipient_id": 2, "content": "encrypted_content", "created_at": "2023-01-01T12:00:00" }`

- `GET /api/messages/user/{user_id}`: Get messages with a specific user
  - Response: `[ { "id": 1, "sender_id": 1, "recipient_id": 2, "content": "Hello!", "created_at": "2023-01-01T12:00:00", "read": true }, ... ]`

- `GET /api/messages/group/{group_id}`: Get messages from a group
  - Response: `[ { "id": 2, "sender": { "id": 1, "username": "user1" }, "content": "Hello group!", "created_at": "2023-01-01T12:00:00" }, ... ]`

- `PUT /api/messages/{message_id}/delivered`: Mark a message as delivered
  - Response: `{ "message": "Message marked as delivered" }`

- `PUT /api/messages/{message_id}/read`: Mark a message as read
  - Response: `{ "message": "Message marked as read" }`
</details>

<details>
<summary>Groups Endpoints</summary>

- `POST /api/group`: Create a new group
  - Request: `{ "name": "Project Team", "members": [2, 3, 4] }`
  - Response: `{ "id": 1, "name": "Project Team", "creator_id": 1, "created_at": "2023-01-01T12:00:00" }`

- `POST /api/group/{group_id}/add`: Add a member to a group
  - Request: `{ "user_id": 5 }`
  - Response: `{ "message": "User added to group" }`

- `GET /api/groups`: Get all groups the user belongs to
  - Response: `[ { "id": 1, "name": "Project Team", "member_count": 4 }, ... ]`

- `GET /api/group/{group_id}`: Get detailed information about a group
  - Response: `{ "id": 1, "name": "Project Team", "members": [ { "id": 1, "username": "user1" }, ... ], "created_at": "2023-01-01T12:00:00" }`

- `DELETE /api/group/{group_id}`: Delete a group
  - Response: `{ "message": "Group deleted successfully" }`
</details>

<details>
<summary>Notifications Endpoints</summary>

- `GET /api/notifications`: Get notification counts
  - Response: `{ "unread_messages": 5, "contact_requests": 2 }`
</details>

---

## 🔧 Technical Implementation Details

<details>
<summary>End-to-End Encryption</summary>

ClearBox implements end-to-end encryption using hybrid cryptography:

1. **Key Generation**:
   - Each user generates an RSA key pair on registration
   - Public keys are stored on the server
   - Private keys are encrypted with the user's password and stored locally

2. **Message Encryption**:
   - Messages are encrypted with AES-256 using a random session key
   - The session key is encrypted with the recipient's public RSA key
   - Both the encrypted message and encrypted session key are sent

3. **Message Decryption**:
   - The recipient decrypts the session key using their private RSA key
   - The message is then decrypted using the session key
</details>

<details>
<summary>Real-time Messaging with MQTT</summary>

The MQTT implementation in ClearBox follows these principles:

1. **Topic Structure**:
   - Individual topics: `user/{user_id}/messages`
   - Group topics: `group/{group_id}/messages`
   - Status topics: `user/{user_id}/status`

2. **Message Format**:
   - JSON payload with encrypted content
   - Metadata for message management

3. **Quality of Service**:
   - QoS 1 (at least once delivery) for messages
   - QoS 0 (at most once delivery) for status updates
</details>

<details>
<summary>Database Schema</summary>

The core database models include:

1. **User**:
   - id, username, email, password_hash, created_at
   - Relationships: contacts, messages, groups

2. **Contact**:
   - id, user_id, contact_id, status, created_at
   - Status: pending, accepted, blocked

3. **Message**:
   - id, sender_id, recipient_id, content, is_group, created_at, delivered, read
   - Content is stored encrypted

4. **Group**:
   - id, name, creator_id, created_at
   - Relationships: members, messages

5. **GroupMember**:
   - id, group_id, user_id, role, joined_at
   - Role: admin, member
</details>

---

## ❓ Troubleshooting

<details>
<summary>Backend Issues</summary>

1. **Database Connection Errors**:
   - Verify PostgreSQL is running: `pg_isready`
   - Check connection string in .env file
   - For development, try using SQLite instead

2. **MQTT Connection Issues**:
   - Verify Mosquitto is running: `systemctl status mosquitto`
   - Check MQTT broker settings in .env
   - Test connection with: `mosquitto_sub -t test`

3. **JWT Authentication Issues**:
   - Verify SECRET_KEY is properly set
   - Check token expiration time
   - Clear browser cookies/local storage
</details>

<details>
<summary>Frontend Issues</summary>

1. **API Connection Errors**:
   - Verify API server is running
   - Check proxy settings in package.json
   - Verify API URLs in services

2. **MQTT Client Issues**:
   - Check browser console for WebSocket errors
   - Verify MQTT broker allows WebSocket connections
   - Check CORS settings

3. **React Rendering Issues**:
   - Clear React cache: `npm run start -- --reset-cache`
   - Check for component key warnings
   - Look for state management issues
</details>

<details>
<summary>Debugging Tips</summary>

1. **Backend Debugging**:
   - Set log level to DEBUG in main.py
   - Use FastAPI's built-in `/docs` endpoint
   - Check application logs

2. **Frontend Debugging**:
   - Use React DevTools
   - Enable source maps
   - Add temporary console.log statements
</details>

---

## 🔒 Security Considerations

<details>
<summary>Expand security details</summary>

1. **Environment Variables**: Keep your `.env` file secure and never commit it to version control.
2. **MQTT Security**: In production, configure Mosquitto with proper authentication and TLS.
3. **JWT Tokens**: Use a strong, random secret key for JWT tokens.
4. **HTTPS**: In production, always use HTTPS for API and frontend.
5. **Password Storage**: Always use bcrypt for password hashing.
6. **SQL Injection**: Use SQLAlchemy's ORM to prevent SQL injection.
7. **XSS Protection**: Sanitize user input on the frontend.
8. **CSRF Protection**: Implement CSRF tokens for form submissions.
9. **Rate Limiting**: Add rate limiting to prevent brute force attacks.
10. **Content Security Policy**: Implement strict CSP headers.
</details>

---

## 📊 GDPR Compliance

<details>
<summary>Expand GDPR compliance details</summary>

ClearBox is designed with GDPR compliance in mind:

1. **User Data Control**: Users can delete their accounts and associated data.
2. **Minimal Data Collection**: Only necessary user information is collected.
3. **Secure Storage**: Passwords are hashed, messages are encrypted.
4. **Transparency**: Users have access to all their data.
5. **Data Portability**: Users can export their data in a common format.
6. **Consent Management**: Clear consent mechanisms for data usage.
7. **Breach Notification**: System for detecting and reporting breaches.
</details>

---

## 🚢 Production Deployment

<details>
<summary>Expand deployment details</summary>

For production deployment, consider the following additional steps:

1. **Use a Production WSGI Server**: Replace the development server with Gunicorn.
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

2. **Configure HTTPS**: Set up SSL certificates for secure communication.
   - Use Let's Encrypt for free SSL certificates
   - Configure proper HSTS headers

3. **MQTT Security**: Configure Mosquitto with user authentication and TLS.
   - Set up username/password authentication
   - Configure TLS/SSL for encrypted connections

4. **Database Optimization**: Set up database indexes and optimization.
   - Add indexes to frequently queried fields
   - Set up connection pooling
   - Configure proper backups

5. **Monitoring**: Implement logging and monitoring solutions.
   - Set up Prometheus/Grafana for metrics
   - Configure centralized logging
   - Set up alerts for critical errors

6. **Frontend Optimization**:
   - Optimize React production build
   - Set up CDN for static assets
   - Implement service workers for offline support

7. **Containerization**:
   - Create Docker containers for each component
   - Set up Docker Compose for local deployment
   - Configure Kubernetes for cloud deployment
</details>

---

## 📈 Scalability

<details>
<summary>Expand scalability details</summary>

ClearBox is designed to be scalable:

1. **Horizontal Scaling**: The stateless API can be deployed across multiple servers.
   - Use a load balancer (nginx, HAProxy)
   - Configure sticky sessions if needed

2. **MQTT Clustering**: Mosquitto can be clustered for high availability.
   - Set up Mosquitto cluster with shared subscriptions
   - Use a load balancer for MQTT connections

3. **Database Scaling**: PostgreSQL supports various scaling strategies.
   - Read replicas for heavy read workloads
   - Connection pooling with PgBouncer
   - Sharding for very large datasets

4. **Caching Layer**:
   - Implement Redis for caching frequently accessed data
   - Cache user presence and status information
   - Store session data centrally

5. **Microservices**:
   - Split into microservices for independent scaling
   - Message service
   - User service
   - Notification service
</details>

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">
  Made with ❤️
</p> 