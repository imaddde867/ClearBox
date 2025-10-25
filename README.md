# ClearBox - Secure Messaging Platform

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)

ClearBox is a secure, scalable, GDPR-compliant messaging application with encryption and real-time communication capabilities.

**[✨ Live Demo: clearbox.live ✨](https://clearbox.live)**

<p align="center">
  <img src="clearbox/frontend/logo/vector/default-monochrome-white.svg" alt="ClearBox Logo" width="400"/>
</p>

## 📸 Screenshots

### Login Screen
![Login Screen](clearbox/frontend/public/screenshots/login.png)

### Chat Interface
![Chat Interface](clearbox/frontend/public/screenshots/chat.png)

### Contacts Management
![Contacts](clearbox/frontend/public/screenshots/contacts.png)

## 🚀 Overview

ClearBox is a full-stack secure messaging platform designed with modern security standards and user privacy at its core. The application enables real-time communication between users, supports group conversations, and ensures message delivery even when recipients are offline.

## ✨ Core Messaging Capabilities

- ** User-to-User Messaging** - Seamless communication between two users with message encryption
- ** Group Chat** - Create and manage conversations with multiple participants simultaneously
- ** Asynchronous Messaging** - Messages are stored and delivered when recipients come online
- ** Read Receipts** - Track message delivery status
- ** Online Status** - See when your contacts are active with real-time presence updates

## 🛡️ Security & Privacy

- ** Encryption** - Messages encrypted using Fernet symmetric encryption (cryptography library)
- ** Secure Authentication** - JWT-based authentication with bcrypt password hashing
- ** Data Minimization** - Only essential information collected and stored
- ** Account Deletion** - User accounts can be deleted (GDPR compliance)
- ** Session Management** - Token-based authentication with proper expiration
- ** HTTPS** - All communications encrypted in transit
- ** Password Protection** - Secure password hashing using bcrypt algorithm

## 📋 GDPR Compliance

ClearBox implements data protection measures in line with GDPR requirements:

- ** Right to Access** - Users can access their profile data
- ** Right to be Forgotten** - Account deletion feature removes user data
- ** Minimal Processing** - Only essential data is collected and processed
- ** Data Security** - Encryption for messages in transit

## 🎯 Key Features

- ** Real-time Notifications** - Instant alerts for new messages and contact requests
- ** Emoji Support** - Express yourself with emoji picker in chat
- ** Responsive Design** - Works on both desktop and mobile devices
- ** User Search** - Find and connect with other users
- ** Typing Indicators** - See when your contacts are typing

## 🛠️ Tech Stack

### Frontend
- **React 18.2.0** - UI library with context API for state management
- **Axios** - HTTP client for API requests
- **MQTT.js** - Client for real-time message handling
- **React Router** - For navigation between different sections
- **CSS3** - Custom styling

### Backend
- **FastAPI 0.104.0** - High-performance Python web framework
- **SQLite** - Database for development
- **PostgreSQL** - Database for production
- **SQLAlchemy 2.0.22** - ORM for database interactions
- **JWT** - Token-based authentication via python-jose
- **MQTT (Mosquitto)** - Message broker for real-time communication
- **Pydantic** - Data validation and settings management
- **Cryptography** - For message encryption

## 📥 Installation Guide

Follow this guide to set up ClearBox on your local machine for development.

### Prerequisites

Before beginning the installation, ensure you have the following installed:

- **Git** - For cloning the repository
- **Python 3.8+** - For the backend server
- **Node.js 14+** - For the frontend application
- **npm 6+** - For package management
- **SQLite** - For development database (included with Python)
- **MQTT Broker** - For real-time messaging (Mosquitto recommended)

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone https://github.com/yourusername/clearbox.git

# Navigate to the project directory
cd clearbox
```

### Step 2: Set Up the Backend

#### Install Python Dependencies

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

#### Configure Environment Variables

Create an `.env` file in the backend directory using the template:

```
# Database
DATABASE_URL=sqlite:///./clearbox.db

# Security
SECRET_KEY=generate_a_secure_random_string_here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883

# Encryption
ENCRYPTION_KEY=generate_another_secure_random_string_here

# Server
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000
```

> **Security Note**: Generate secure random strings for SECRET_KEY and ENCRYPTION_KEY using:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### Step 3: Set Up the MQTT Broker

#### Install Mosquitto MQTT Broker

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

**On macOS:**
```bash
brew install mosquitto
brew services start mosquitto
```

**On Windows:**
1. Download the installer from [mosquitto.org/download](https://mosquitto.org/download/)
2. Follow the installation wizard
3. Start the Mosquitto service from Windows Services

#### Configure Mosquitto with WebSocket Support

Create a file named `mosquitto.conf`:

```
# MQTT over TCP
listener 1883
allow_anonymous true

# MQTT over WebSockets
listener 9001
protocol websockets
allow_anonymous true
```

Start Mosquitto with this configuration:
```bash
mosquitto -c mosquitto.conf
```

### Step 4: Set Up the Frontend

```bash
# Navigate to the frontend directory from the project root
cd ../frontend

# Install Node.js dependencies
npm install
```

#### Configure Frontend Environment

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MQTT_URL=ws://localhost:9001
```

### Step 5: Start the Application

#### Start the Backend Server

```bash
# Ensure you're in the backend directory with the virtual environment activated
cd ../backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the server
python run.py
```

The backend server will start at http://localhost:8000 with API documentation available at http://localhost:8000/docs.

#### Start the Frontend Development Server

```bash
# In a new terminal, navigate to the frontend directory
cd ../frontend

# Start the React development server
npm start
```

The frontend will be available at http://localhost:3000.

### Step 6: Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

Create a new account or log in with existing credentials.

## 📂 Project Structure

```
clearbox/
├── backend/               # FastAPI backend server
│   ├── app/               # Application code
│   │   ├── routes/        # API endpoints
│   │   ├── models.py      # Database models
│   │   ├── mqtt_client.py # MQTT integration
│   │   ├── encryption.py  # Message encryption
│   │   └── ...
│   ├── migrations/        # Database migrations
│   └── requirements.txt   # Python dependencies
└── frontend/              # React frontend
    ├── src/               # Source code
    │   ├── components/    # UI components
    │   ├── contexts/      # State management
    │   └── services/      # API communication
    └── package.json       # Node.js dependencies
```

## 📚 Resources & References

The development of ClearBox was made possible thanks to the following resources and documentation:

- **FastAPI Documentation** - [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **React.js Documentation** - [https://reactjs.org/docs/getting-started.html](https://reactjs.org/docs/getting-started.html)
- **PostgreSQL Documentation** - [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- **SQLAlchemy Documentation** - [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)
- **MQTT Documentation** - [https://mqtt.org/](https://mqtt.org/)
- **Python Cryptography Library** - [https://cryptography.io/en/latest/](https://cryptography.io/en/latest/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

© 2025 ClearBox - Created by Imad 

## Quick Start Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/imaddde867/clearbox.git
   cd clearbox
   ```

2. **Set up the backend:**
   ```bash
   cd backend
   
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file from template
   cp .env.template .env
   
   # Edit the .env file and generate secure keys:
   # SECRET_KEY and ENCRYPTION_KEY using:
   # python -c "import secrets; print(secrets.token_hex(32))"
   
   # Start the backend server
   python run.py
   ```

3. **Set up the MQTT broker:**
   ```bash
   # Install Mosquitto
   # On macOS:
   brew install mosquitto
   
   # On Ubuntu:
   # sudo apt install mosquitto
   
   # Create a configuration file
   echo -e "# MQTT over TCP\nlistener 1883\nallow_anonymous true\n\n# MQTT over WebSockets\nlistener 9001\nprotocol websockets\nallow_anonymous true" > mosquitto.conf
   
   # Run Mosquitto with this configuration
   mosquitto -c mosquitto.conf
   ```

4. **Set up the frontend:**
   ```bash
   cd ../frontend
   
   # Install dependencies
   npm install
   
   # Start the development server
   npm start
   ```

5. **Access the application:**
   Open your browser and navigate to http://localhost:3000

## Repository Structure

- `clearbox/backend` - FastAPI backend server
- `clearbox/frontend` - React frontend application
- `clearbox/docs` - Data Engineering Documentation

## Data Engineering Documentation

This project includes comprehensive data engineering documentation:

- **Database Schema** (`clearbox/docs/database_schema.md`) - Detailed model of the relational database with entity relationships
- **Database Diagram** (`clearbox/docs/database.png`) - Visual representation of the database schema
- **System Architecture** (`clearbox/docs/system_architecture_diagram.md`) - Documentation of the layered system architecture
- **Architecture Diagram** (`clearbox/docs/diagram.png`) - Visual representation of data flow through system layers

These documents illustrate how the application handles data storage, retrieval, and real-time messaging capabilities.

## Development Notes

- The application uses SQLite by default for development
- MQTT broker runs locally for real-time messaging
- All API endpoints are available at http://localhost:8000/api
- API documentation is available at http://localhost:8000/docs

## License

This project is licensed under the MIT License.
