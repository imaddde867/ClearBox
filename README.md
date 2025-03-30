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

- **💬 User-to-User Messaging** - Seamless communication between two users with message encryption
- **👨‍👩‍👧‍👦 Group Chat** - Create and manage conversations with multiple participants simultaneously
- **📴 Asynchronous Messaging** - Messages are stored and delivered when recipients come online
- **📬 Read Receipts** - Track message delivery status
- **👀 Online Status** - See when your contacts are active with real-time presence updates

## 🛡️ Security & Privacy

- **🔒 Encryption** - Messages encrypted using Fernet symmetric encryption (cryptography library)
- **🔐 Secure Authentication** - JWT-based authentication with bcrypt password hashing
- **🕵️ Data Minimization** - Only essential information collected and stored
- **🗑️ Account Deletion** - User accounts can be deleted (GDPR compliance)
- **⏲️ Session Management** - Token-based authentication with proper expiration
- **🔐 HTTPS** - All communications encrypted in transit (production environment)
- **🛡️ Password Protection** - Secure password hashing using bcrypt algorithm

## 📋 GDPR Compliance

ClearBox implements data protection measures in line with GDPR requirements:

- **🔍 Right to Access** - Users can access their profile data
- **🗑️ Right to be Forgotten** - Account deletion feature removes user data
- **⚖️ Minimal Processing** - Only essential data is collected and processed
- **🔒 Data Security** - Encryption for messages in transit

## 📈 Scalability Architecture

ClearBox is designed with scalability features:

- **🌐 Stateless API** - FastAPI backend with stateless design
- **📨 Message Broker** - MQTT for real-time message delivery
- **🗃️ Database Design** - SQL database with proper indexing and relationships
- **🔌 WebSocket Management** - Efficient handling of client connections
- **📊 Load Balancing** - Architecture supports distribution via Nginx

## 🎯 Key Features

- **🔔 Real-time Notifications** - Instant alerts for new messages and contact requests
- **😊 Emoji Support** - Express yourself with emoji picker in chat
- **📱 Responsive Design** - Works on both desktop and mobile devices
- **🔍 User Search** - Find and connect with other users
- **⌨️ Typing Indicators** - See when your contacts are typing

## 🛠️ Tech Stack

### Frontend
- **React 18.2.0** - UI library with context API for state management
- **Axios** - HTTP client for API requests
- **MQTT.js** - Client for real-time message handling
- **React Router** - For navigation between different sections
- **CSS3** - Custom styling

### Backend
- **FastAPI 0.104.0** - High-performance Python web framework
- **PostgreSQL** - Primary database for production
- **SQLite** - Database for development
- **SQLAlchemy 2.0.22** - ORM for database interactions
- **JWT** - Token-based authentication via python-jose
- **MQTT (Mosquitto)** - Message broker for real-time communication
- **Pydantic** - Data validation and settings management
- **Cryptography** - For message encryption

### Deployment
- **AWS EC2** - Cloud hosting
- **Nginx** - Web server and reverse proxy
- **Let's Encrypt** - SSL certificate provider
- **Systemd** - Service management

## 📥 Installation Guide

Follow this guide to set up ClearBox on your local machine for development or your own server for production.

### Prerequisites

Before beginning the installation, ensure you have the following installed:

- **Git** - For cloning the repository
- **Python 3.8+** - For the backend server
- **Node.js 14+** - For the frontend application
- **npm 6+** - For package management
- **PostgreSQL 12+** - For production database
- **SQLite** - For development database (included with Python)
- **MQTT Broker** - For real-time messaging (Mosquitto recommended)

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/imaddde867/clearbox.git

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

#### Set Up the Database

For development (SQLite - simplest option):
```bash
# SQLite database will be created automatically when running the app
```

For production (PostgreSQL):
```bash
# Connect to PostgreSQL
psql -U postgres

# Create a database
CREATE DATABASE clearbox;

# Create a dedicated user
CREATE USER clearbox_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE clearbox TO clearbox_user;

# Exit PostgreSQL
\q
```

#### Configure Environment Variables

Create an `.env` file in the backend directory using the template:

For development (SQLite):
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

For production (PostgreSQL):
```
# Database
DATABASE_URL=postgresql://clearbox_user:your_secure_password@localhost/clearbox

# Security
SECRET_KEY=generate_a_secure_random_string_here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=your_mqtt_username
MQTT_PASSWORD=your_mqtt_password
MQTT_USE_TLS=true

# Encryption
ENCRYPTION_KEY=generate_another_secure_random_string_here

# Server
PORT=8000
ENVIRONMENT=production
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
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

For development:
```
# MQTT over TCP
listener 1883
allow_anonymous true

# MQTT over WebSockets
listener 9001
protocol websockets
allow_anonymous true
```

For production:
```
# MQTT over TCP
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd

# MQTT over WebSockets
listener 9001
protocol websockets
allow_anonymous false
password_file /etc/mosquitto/passwd
```

Start Mosquitto with this configuration:
```bash
# For development
mosquitto -c mosquitto.conf

# For production (using the system service)
sudo cp mosquitto.conf /etc/mosquitto/conf.d/clearbox.conf
sudo systemctl restart mosquitto
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

For development:
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MQTT_URL=ws://localhost:9001
```

For production:
```
REACT_APP_API_URL=https://your-domain.com/api
REACT_APP_MQTT_URL=wss://your-domain.com/mqtt
```

#### Check API Proxy Configuration

The frontend uses a proxy setting in `package.json` to forward API requests to the backend. Make sure the proxy setting matches your backend URL:

```json
{
  "name": "clearbox-frontend",
  "proxy": "http://localhost:8000"
}
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

## 💻 Development Tools & Tips

### Building for Production

#### Backend

```bash
# Make sure your virtual environment is activated and requirements are installed
cd backend
source venv/bin/activate
```

Create a systemd service file (for Linux servers):
```ini
[Unit]
Description=ClearBox Backend
After=network.target postgresql.service

[Service]
User=your_username
WorkingDirectory=/path/to/clearbox/backend
Environment="PATH=/path/to/clearbox/backend/venv/bin"
ExecStart=/path/to/clearbox/backend/venv/bin/python run.py --port 8000

[Install]
WantedBy=multi-user.target
```

#### Frontend

```bash
# Create optimized production build
cd frontend
npm run build

# The build folder will contain static files to be served by Nginx
```

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
├── frontend/              # React frontend
│   ├── src/               # Source code
│   │   ├── components/    # UI components
│   │   ├── contexts/      # State management
│   │   └── services/      # API communication
│   └── package.json       # Node.js dependencies
├── scripts/               # Utility scripts
├── deploy/                # Deployment configurations
└── deploy-package/        # Deployment packages
```

## 📦 Deployment Documentation

ClearBox is deployed on AWS EC2 with the following configuration:

1. **Server Setup**
   - Amazon Linux 2023 OS
   - Nginx as reverse proxy
   - PostgreSQL database
   - Mosquitto MQTT broker (if configured)

2. **Domain and SSL**
   - Domain configured with DNS provider (name.com)
   - SSL certificate via Let's Encrypt
   - HTTP to HTTPS redirection

3. **Application Deployment**
   - Backend runs as a systemd service (clearbox-backend.service)
   - Frontend served as static files through Nginx
   - API requests proxied to the backend on port 8000

4. **Nginx Configuration**
   - Serves static frontend files from /home/ec2-user/ClearBox/clearbox/frontend/build
   - Proxies API requests to http://localhost:8000
   - Handles SSL termination

5. **Systemd Service**
   - Manages the backend service
   - Ensures automatic startup on server boot
   - Handles logging and process management


## 🔮 Upcoming Features

ClearBox is actively being developed with the following enhancements planned for future releases:

- **🔑 Improved Authentication**
  - Detailed login/register error explanations
  - Social media authentication options
  - Two-factor authentication (2FA)

- **📁 File Sharing**
  - Image and document attachments
  - File previews and thumbnails
  - Secure file encryption

- **🎤 Rich Media**
  - Voice messages
  - Audio calling
  - Video chat capabilities

- **🛠️ User Experience**
  - Message reactions with emoji
  - Message editing and deletion
  - Enhanced mobile experience

- **🌍 Internationalization**
  - Multi-language support
  - Regional formatting

Stay tuned for these exciting updates to make your ClearBox experience even better!


## 📊 AWS Free Tier Optimization

ClearBox is now configured to operate entirely within AWS Free Tier limits with zero cost:

- **EC2 Instance:** Uses t3.micro instance (free for 750 hours/month for 12 months)
- **Storage:** 8GB EBS volume (free up to 30GB for 12 months)
- **Database:** Using PostgreSQL on the EC2 instance instead of RDS
- **DNS Management:** Using domain registrar's free DNS service instead of Route 53
- **MQTT Broker:** Running in a Docker container on the EC2 instance
- **Data Transfer:** Optimized to stay within 100GB/month free outbound data

**Cost Optimization Measures:**
- Removed all RDS snapshots that were incurring charges
- Migrated from Route 53 ($0.50/month) to free DNS at the domain registrar
- Set up billing alarm to notify at $1 threshold
- EC2 instance configured for optimal free tier resource usage

This configuration ensures ClearBox can run with $0 AWS cost during the 12-month free tier period.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

© 2025 ClearBox - Created by Imad 