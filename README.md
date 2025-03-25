# ClearBox - Secure Messaging App

ClearBox is a secure, scalable, GDPR-compliant messaging app built with Python (FastAPI) and React. It features real-time messaging using MQTT, end-to-end encryption, and a modern dark-themed UI.

## Features

- **Secure Authentication**: User registration and JWT-based authentication
- **Contact Management**: Search for users, send/accept contact requests
- **Real-time Messaging**: One-on-one chats and group conversations
- **End-to-End Encryption**: Messages are encrypted using Python's cryptography library
- **Notifications**: Real-time notifications for new messages and contact requests
- **GDPR Compliance**: Users can delete their accounts and data
- **Modern UI**: Futuristic, dark-themed interface built with React

## Code Optimization

The codebase has been optimized for better performance and maintainability:

- Removed unnecessary temporary and backup files
- Cleaned up Python cache directories and compiled .pyc files
- Removed trailing whitespace and fixed indentation
- Ensured consistent coding style throughout the project
- Removed redundant blank lines while preserving logical separation
- Optimized imports and dependencies

## Technologies Used

- **Backend**: Python 3.8+, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, React Router, Axios
- **Real-time Messaging**: MQTT (Mosquitto), paho-mqtt
- **Security**: JWT tokens, Cryptography library, Bcrypt
- **Deployment**: Docker (optional)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Node.js 14 or higher
- PostgreSQL
- Mosquitto MQTT Broker

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/clearbox.git
cd clearbox
```

### 2. Set Up the Backend

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

```
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost/clearbox

# JWT Authentication
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Encryption
ENCRYPTION_KEY=your_encryption_key_here

# MQTT Configuration
MQTT_BROKER=localhost
MQTT_PORT=1883

# Server Configuration
PORT=8000
```

Make sure to replace the placeholders with your actual values.

#### Create the Database

```sql
CREATE DATABASE clearbox;
```

The application will automatically create all the necessary tables when started.

### 3. Set Up the MQTT Broker (Mosquitto)

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

```
listener 1883
allow_anonymous true
```

### 4. Set Up the Frontend

```bash
cd ../frontend
npm install
```

## Running the Application

### 1. Start the Backend

```bash
cd backend
python run.py --reload
```

The API will be available at http://localhost:8000.

### 2. Start the Frontend

```bash
cd frontend
npm start
```

The frontend will be available at http://localhost:3000.

## API Endpoints

### Authentication

- `POST /api/signup`: Register a new user
- `POST /api/login`: Get an access token
- `GET /api/profile`: Get the current user's profile
- `DELETE /api/user`: Delete the current user's account

### Contacts

- `GET /api/search?query={query}`: Search for users
- `POST /api/contact/request`: Send a contact request
- `GET /api/contact/requests`: Get pending contact requests
- `POST /api/contact/accept/{request_id}`: Accept a contact request
- `POST /api/contact/deny/{request_id}`: Deny a contact request
- `GET /api/contacts`: Get all contacts

### Messages

- `POST /api/messages`: Send a message (to user or group)
- `GET /api/messages/user/{user_id}`: Get messages with a specific user
- `GET /api/messages/group/{group_id}`: Get messages from a group
- `PUT /api/messages/{message_id}/delivered`: Mark a message as delivered

### Groups

- `POST /api/group`: Create a new group
- `POST /api/group/{group_id}/add`: Add a member to a group
- `GET /api/groups`: Get all groups the user belongs to
- `GET /api/group/{group_id}`: Get detailed information about a group
- `DELETE /api/group/{group_id}`: Delete a group

### Notifications

- `GET /api/notifications`: Get notification counts

## Security Considerations

1. **Environment Variables**: Keep your `.env` file secure and never commit it to version control.
2. **MQTT Security**: In production, configure Mosquitto with proper authentication and TLS.
3. **JWT Tokens**: Use a strong, random secret key for JWT tokens.
4. **HTTPS**: In production, always use HTTPS for API and frontend.

## GDPR Compliance

ClearBox is designed with GDPR compliance in mind:

1. **User Data Control**: Users can delete their accounts and associated data.
2. **Minimal Data Collection**: Only necessary user information is collected.
3. **Secure Storage**: Passwords are hashed, messages are encrypted.
4. **Transparency**: Users have access to all their data.

## Production Deployment

For production deployment, consider the following additional steps:

1. **Use a Production WSGI Server**: Replace the development server with Gunicorn.
2. **Configure HTTPS**: Set up SSL certificates for secure communication.
3. **MQTT Security**: Configure Mosquitto with user authentication and TLS.
4. **Database Optimization**: Set up database indexes and optimization.
5. **Monitoring**: Implement logging and monitoring solutions.

## Scalability

ClearBox is designed to be scalable:

1. **Horizontal Scaling**: The stateless API can be deployed across multiple servers.
2. **MQTT Clustering**: Mosquitto can be clustered for high availability.
3. **Database Scaling**: PostgreSQL supports various scaling strategies.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 