# ClearBox — Secure Messaging Platform

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)

ClearBox is a secure, scalable, GDPR-compliant messaging application with real-time communication and practical encryption.

**Live Demo:** [clearbox.live](https://clearbox.live)

<p align="center">
  <img src="clearbox/frontend/logo/vector/default-monochrome-white.svg" alt="ClearBox Logo" width="400"/>
</p>

---

## Screenshots

**Login Screen**
![Login Screen](clearbox/frontend/public/screenshots/login.png)

**Chat Interface**
![Chat Interface](clearbox/frontend/public/screenshots/chat.png)

**Contacts Management**
![Contacts](clearbox/frontend/public/screenshots/contacts.png)

---

## Overview

ClearBox is a full-stack messaging platform built with privacy by design. It supports 1:1 and group conversations, delivers messages in real time, and reliably syncs pending messages when users come back online.

---

## Core Messaging Capabilities

* **User-to-User Messaging** — Encrypted, seamless 1:1 chat
* **Group Chat** — Create conversations with multiple participants and roles
* **Asynchronous Delivery** — Store-and-forward for offline users
* **Read Receipts** — Delivery and read status tracking
* **Online Presence** — Real-time status and typing indicators

---

## Security & Privacy

* **Encryption** — Fernet symmetric encryption (cryptography) for message payloads
* **Authentication** — JWT-based sessions; passwords hashed with bcrypt
* **Session Controls** — Token expiry and refresh; strict CORS and HTTPS
* **Data Minimization** — Only essential user data is collected and stored
* **Account Deletion** — Users can delete their accounts and associated data

---

## GDPR Alignment

* **Right of Access** — Users can access profile data
* **Right to Erasure** — Account deletion removes user data
* **Purpose Limitation** — Minimal processing of necessary fields only
* **Security Measures** — Encryption in transit and at rest for message content

---

## Tech Stack

**Frontend**

* React 18.2 (Context API for state)
* Axios
* MQTT.js (WebSocket client)
* React Router
* CSS3

**Backend**

* FastAPI 0.104
* SQLAlchemy 2.0.22
* SQLite (development), PostgreSQL (production)
* JWT via `python-jose`
* MQTT (Mosquitto) for real-time delivery
* Pydantic
* cryptography

---

## Installation (Local Development)

### Prerequisites

* Git
* Python 3.8+
* Node.js 14+ and npm
* SQLite (dev) or PostgreSQL (prod)
* MQTT broker (Mosquitto recommended)

### 1) Clone

```bash
git clone https://github.com/imaddde867/ClearBox.git
cd ClearBox
```

### 2) Backend Setup

```bash
cd backend
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
# venv\Scripts\activate

pip install -r requirements.txt
cp .env.template .env
```

Edit `.env`:

```
# Database
DATABASE_URL=sqlite:///./clearbox.db

# Security
SECRET_KEY=<secure_64_hex>
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883

# Encryption
ENCRYPTION_KEY=<secure_64_hex>

# Server
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000
```

Generate secure keys:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Start the API:

```bash
python run.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 3) MQTT Broker (Mosquitto)

Create `mosquitto.conf`:

```
# MQTT over TCP
listener 1883
allow_anonymous true

# MQTT over WebSockets
listener 9001
protocol websockets
allow_anonymous true
```

Start Mosquitto:

```bash
mosquitto -c mosquitto.conf
```

### 4) Frontend Setup

```bash
cd ../frontend
npm install
```

Create `frontend/.env`:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MQTT_URL=ws://localhost:9001
```

Run the dev server:

```bash
npm start
# Frontend: http://localhost:3000
```

---

## Project Structure

```
clearbox/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── models.py        # ORM models
│   │   ├── mqtt_client.py   # MQTT integration
│   │   ├── encryption.py    # Message encryption
│   │   └── ...
│   ├── migrations/
│   └── requirements.txt
└── frontend/                # React frontend
    ├── src/
    │   ├── components/
    │   ├── contexts/
    │   └── services/
    └── package.json
```

---

## Data Engineering Documentation

* **Database Schema** — `clearbox/docs/database_schema.md`
* **Database Diagram** — `clearbox/docs/database.png`
* **System Architecture** — `clearbox/docs/system_architecture_diagram.md`
* **Architecture Diagram** — `clearbox/docs/diagram.png`

---

## Development Notes

* SQLite by default for development; PostgreSQL recommended for production
* Local Mosquitto broker for real-time messaging
* API base: `http://localhost:8000/api`
* OpenAPI docs: `http://localhost:8000/docs`

---

## License

This project is released under the MIT License. See the `LICENSE` file for details.

---

© 2025 ClearBox — Created by Imad
