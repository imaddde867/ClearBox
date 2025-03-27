# ClearBox - Secure Messaging Platform

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![React](https://img.shields.io/badge/React-18.x-61DAFB.svg)

ClearBox is a secure, scalable, GDPR-compliant messaging application with end-to-end encryption and real-time communication capabilities.

**[✨ Live Demo: clearbox.live ✨](https://clearbox.live)**

<p align="center">
  <img src="clearbox/frontend/logo/vector/default-monochrome-white.svg" alt="ClearBox Logo" width="400"/>
</p>

## 📸 Screenshots

### Login Screen
![Login Screen](clearbox/rontend/public/screenshots/login.png)

### Chat Interface
![Chat Interface](clearbox/frontend/public/screenshots/chat.png)

### Contacts Management
![Contacts](clearbox/frontend/public/screenshots/contacts.png)

## 🚀 Overview

ClearBox is a full-stack secure messaging platform designed with modern security standards and user privacy at its core. The application enables real-time communication between users, supports group conversations, and ensures message delivery even when recipients are offline.

## ✨ Core Messaging Capabilities

- **💬 User-to-User Messaging** - Seamless, encrypted communication between two users
- **👨‍👩‍👧‍👦 Group Chat** - Create and manage conversations with multiple participants simultaneously
- **📴 Asynchronous Messaging** - Messages are delivered when recipients come online; no message loss
- **📬 Read Receipts** - Know when your messages have been delivered and read
- **👀 Online Status** - See when your contacts are active or last seen

## 🛡️ Security & Privacy

- **🔒 End-to-End Encryption** - All messages encrypted using industry-standard cryptography
- **🔐 Secure Authentication** - JWT-based authentication with secure password hashing
- **🕵️ Data Minimization** - Only essential information collected and stored
- **🗑️ Account Deletion** - Full ability to delete account and all associated data
- **⏲️ Session Management** - Secure token handling with proper expiration
- **🔐 HTTPS** - All communications encrypted in transit
- **🛡️ Password Protection** - Strong password hashing using modern algorithms

## 📋 GDPR Compliance

ClearBox implements comprehensive data protection measures in line with GDPR requirements:

- **🔍 Right to Access** - Users can access all their data via the profile interface
- **🗑️ Right to be Forgotten** - Account deletion feature permanently removes all user data
- **📤 Data Portability** - Export feature allows users to download their message history
- **✅ Consent Management** - Clear opt-in mechanisms for data collection
- **⚖️ Minimal Processing** - Only essential data is collected and processed
- **🔒 Data Security** - Encryption in transit and at rest protects user information
- **🚨 Breach Notification** - Systems in place to detect and report data breaches

## 📈 Scalability Architecture

ClearBox is designed with scalability in mind:

- **🌐 Stateless API** - Horizontally scalable FastAPI backend
- **📨 Message Broker** - MQTT enables message distribution across multiple server instances
- **🗃️ Database Design** - Optimized schema with proper indexing for high-volume queries
- **🔌 Connection Management** - Efficient handling of client connections
- **⚡ Caching Strategy** - Implementation of strategic caching for frequently accessed data
- **📊 Load Balancing** - Architecture supports distribution across multiple servers

## 🎯 Additional Features

- **🔔 Real-time Notifications** - Instant alerts for new messages and contact requests
- **😊 Rich Emoji Support** - Express yourself with a comprehensive emoji picker
- **🎨 Dark Theme** - Modern, eye-friendly interface with sleek design
- **📱 Responsive Design** - Works seamlessly on both desktop and mobile devices
- **🔍 User Search** - Find and connect with other users easily
- **🖼️ File Sharing** - Share images and files with your contacts
- **🔗 Link Preview** - Rich previews when sharing URLs in chats
- **⌨️ Typing Indicators** - See when your contacts are typing

## 🛠️ Tech Stack

### Frontend
- **React** - UI library with context API for state management
- **Axios** - HTTP client for API requests
- **MQTT.js** - Client for real-time message handling
- **CSS3** - Custom styling with advanced animations

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Primary database
- **SQLAlchemy** - ORM for database interactions
- **JWT** - Token-based authentication
- **MQTT (Mosquitto)** - Message broker for real-time communication

### Deployment
- **AWS EC2** (t2.micro) - Cloud hosting within AWS free tier
- **Nginx** - Web server and reverse proxy
- **Let's Encrypt** - SSL certificate provider
- **Route 53** - DNS management

## 📥 Complete Installation Guide

Follow this comprehensive guide to set up ClearBox on your local machine for development or your own server for production.

### Prerequisites

Before beginning the installation, ensure you have the following installed:

- **Git** - For cloning the repository (version 2.x+)
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

# Verify installation
pip list
```

#### Set Up the Database

For development (SQLite - simplest option):
```bash
# SQLite database will be created automatically
# No additional steps required
```

For production (PostgreSQL):
```bash
# Connect to PostgreSQL
psql -U postgres

# Create a database
CREATE DATABASE clearbox;

# Create a dedicated user (optional but recommended)
CREATE USER clearbox_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE clearbox TO clearbox_user;

# Exit PostgreSQL
\q
```

#### Configure Environment Variables

```bash
# Create an environment file from the template
cp .env.example .env
```

Edit the `.env` file with your preferred text editor and configure:

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
PORT=8001
DEBUG=True
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

# Encryption
ENCRYPTION_KEY=generate_another_secure_random_string_here

# Server
PORT=8001
DEBUG=False
```

> **Security Note**: Generate secure random strings for SECRET_KEY and ENCRYPTION_KEY using:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

#### Initialize the Database

```bash
# Ensure your virtual environment is activated
# Run the database initialization script
python run.py init_db

# Create a test user (optional)
python run.py create_user --username test --password test123 --email test@example.com
```

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

Create a file named `mosquitto.conf` in an appropriate location:

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

# Optional: Enable TLS for WebSockets
# listener 9001
# protocol websockets
# cafile /etc/mosquitto/ca_certificates/ca.crt
# certfile /etc/mosquitto/certs/server.crt
# keyfile /etc/mosquitto/certs/server.key
# require_certificate false
# allow_anonymous false
# password_file /etc/mosquitto/passwd
```

Start Mosquitto with this configuration:
```bash
# For development
mosquitto -c mosquitto.conf

# For production (using the system service)
sudo cp mosquitto.conf /etc/mosquitto/conf.d/clearbox.conf
sudo systemctl restart mosquitto
```

If you're using password authentication, create a password file:
```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd mqtt_user
# Enter password when prompted
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
REACT_APP_API_URL=http://localhost:8001
REACT_APP_MQTT_URL=ws://localhost:9001
REACT_APP_ENV=development
```

For production:
```
REACT_APP_API_URL=https://your-domain.com/api
REACT_APP_MQTT_URL=wss://your-domain.com/mqtt
REACT_APP_ENV=production
```

#### Important: Check API Proxy Configuration

The frontend uses a proxy setting in `package.json` to forward API requests to the backend. Make sure the proxy setting points to the correct backend URL:

Open `frontend/package.json` and check that the proxy setting matches your backend URL:

```json
{
  "name": "clearbox-frontend",
  // ...other settings...
  "proxy": "http://localhost:8001"
}
```

If your backend runs on a different port (e.g., 8000), update this setting accordingly.

### Step 5: Start the Application

#### Start the Backend Server

```bash
# Ensure you're in the backend directory with the virtual environment activated
cd ../backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# For development with auto-reload
python run.py --reload

# For production
python run.py
```

The backend server will start at http://localhost:8001 with API documentation available at http://localhost:8001/docs.

> **Alternative Backend Start Method**: If the above command doesn't work, you can try:
> ```bash
> python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
> ```

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

Create a new account or log in with the test user if you created one.

### Step 7: Troubleshooting Common Issues

If you encounter problems with the installation or running the application, here are some common issues and their solutions:

#### Backend Issues

1. **Port Conflicts**: If port 8001 is already in use, you can change it in the `.env` file. Remember to update the proxy setting in `frontend/package.json` to match.

2. **Backend Connection Errors**:
   - Verify the backend is running by checking `http://localhost:8001/docs` in your browser
   - Make sure ports match between backend server and frontend proxy setting
   - Check the backend console for detailed error logs

3. **Database Errors**:
   - For SQLite: Ensure the backend has write permissions to create the database file
   - For PostgreSQL: Verify the database exists and credentials are correct

4. **Python Command Not Found**:
   - Ensure your virtual environment is activated
   - Try using `python3` instead of `python` on some systems

#### Frontend Issues

1. **API Connection Problems**:
   - The most common issue is a port mismatch between backend and frontend
   - Open browser DevTools (F12) and check the Network tab for failed API requests
   - Verify in `package.json` that the "proxy" field points to the right backend URL/port
   - Check for CORS errors in the console

2. **Login/Signup Failures**:
   - If you see 500 errors in browser console, check backend logs for details
   - Verify the backend is running and accessible at the expected port
   - Check if the API endpoints match between frontend and backend

3. **MQTT Connection Issues**:
   - Ensure the Mosquitto broker is running and WebSocket support is enabled
   - Verify WebSocket port (9001) is accessible
   - Check browser console for WebSocket connection errors

#### Quick Fix for Common Port Issue

If you're experiencing login or API connection issues, the most common problem is a port mismatch. The default configuration in this README uses port 8001, but your system might be configured differently.

Here's how to identify and fix this:

1. Check which port your backend is running on (look for "Uvicorn running on http://0.0.0.0:XXXX" in the terminal)
2. Open `frontend/package.json` and update the "proxy" field to match that port:
   ```json
   "proxy": "http://localhost:XXXX"
   ```
3. Restart the frontend development server (stop with Ctrl+C, then run `npm start` again)

## 💻 Development Tools & Tips

### Running Tests

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

#### Backend

```bash
# Make sure your virtual environment is activated and requirements are installed
cd backend
source venv/bin/activate
pip install gunicorn  # For production WSGI server
```

Create a systemd service file (for Linux servers):
```ini
[Unit]
Description=ClearBox Backend
After=network.target

[Service]
User=your_username
Group=your_groupname
WorkingDirectory=/path/to/clearbox/backend
Environment="PATH=/path/to/clearbox/backend/venv/bin"
ExecStart=/path/to/clearbox/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8001 run:app

[Install]
WantedBy=multi-user.target
```

#### Frontend

```bash
# Create optimized production build
cd frontend
npm run build

# The build folder will contain static files to be served
```

### Local Production Simulation

```bash
# Serve the production build locally
cd frontend
npx serve -s build
```

## 📂 Project Structure

```
clearbox/
├── backend/               # FastAPI backend server
│   ├── app/               # Application code
│   │   ├── routes/        # API endpoints
│   │   ├── models.py      # Database models
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
└── deploy/                # Deployment configuration
```

## 📦 Deployment Documentation

ClearBox is deployed on AWS EC2 using a t2.micro instance (AWS Free Tier eligible) with the following configuration:

1. **Server Setup**
   - Amazon Linux 2023 OS
   - Nginx as reverse proxy
   - PostgreSQL database
   - Mosquitto MQTT broker

2. **Domain and SSL**
   - Domain configured with Route 53
   - SSL certificate via Let's Encrypt
   - Automatic HTTP to HTTPS redirection

3. **Application Deployment**
   - Backend runs as a systemd service
   - Frontend served as static files through Nginx
   - API requests proxied to the backend
   
4. **Deployment Script**
   ```bash
   # Deploy backend
   cd ~/ClearBox/clearbox/backend
   git pull
   source venv/bin/activate
   pip install -r requirements.txt
   sudo systemctl restart clearbox
   
   # Deploy frontend
   cd ~/ClearBox/clearbox/frontend
   git pull
   npm install
   npm run build
   sudo cp -r build/* /var/www/html/
   sudo systemctl restart nginx
   ```

## 🆕 Recent Updates

- **March 27, 2025**
  - Fixed infinite loading issue on the contacts page
  - Improved error handling when backend is unreachable
  - Added timeout for loading indicators
  - Updated API endpoints to use relative URLs
  - Fixed DNS configuration for the production server

- **March 26, 2025**
  - Implemented end-to-end encryption for all messages
  - Added group chat functionality
  - Enhanced UI with animations and transitions
  - Optimized database queries for better performance

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

© 2025 ClearBox - Created by Imad 