# ClearBox: GDPR-Compliant Secure Messaging Platform
<p align="center">
  <img src="docs/Logo/Logo_white.png" alt="ClearBox Logo" width="25%"/>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![RabbitMQ](https://img.shields.io/badge/Message%20Broker-RabbitMQ-FF6600)](https://www.rabbitmq.com/)


A scalable, secure, and GDPR-compliant chat application supporting 1:1 messaging, group chats, and offline message delivery.  Built with message queues, end-to-end encryption, and real-time communication.

---

## ✨ Features

- **Real-time Messaging:** WebSocket-based instant delivery for online users.
- **Offline Support:** Messages are queued in RabbitMQ for asynchronous delivery.
- **End-to-End Encryption (E2EE):** Securely encrypts messages using the Signal Protocol.
- **GDPR Compliance:** Implements user data anonymization, deletion workflows, and comprehensive audit logging.
- **Group Chats:** Enables creation and messaging within groups.
- **Presence Status:** Tracks online/offline users via Redis caching.
- **Scalable Backend:** Designed for horizontal scaling using Docker and Kubernetes.

---

## 🛠️ Tech Stack

| Category       | Tools/Technologies                                      |
|----------------|---------------------------------------------------------|
| Backend        | Python (FastAPI), Node.js (Express), Go                 |
| Database       | PostgreSQL (ACID compliance), MongoDB (message history) |
| Message Broker | RabbitMQ (offline queues), Apache Kafka (scaling)       |
| Caching        | Redis (user presence, session management)               |
| Real-time      | WebSocket (Socket.IO, `websockets` library)             |
| Security       | TLS 1.3, JWT, OAuth 2.0, Signal Protocol (E2EE)         |
| Frontend       | React (sample client)                                   |
| DevOps         | Docker, Kubernetes, Nginx (load balancing), AWS/GCP     |
| Monitoring     | Prometheus + Grafana, ELK Stack (logging)               |

---

## 📐 Architecture Diagram

![Architecture Diagram](docs/Plan_Diagram.drawio.png)
*Detailed architecture diagram available in [ARCHITECTURE.md](docs/architecture.md).*

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ / Node.js 18+
- Docker (for RabbitMQ, Redis, PostgreSQL)
- `pip`

### Setup

1. **Clone:** `git clone https://github.com/yourusername/clearbox.git && cd clearbox`
2. **Start Dependencies (Docker):** `docker-compose up -d rabbitmq redis postgres`
3. **Backend Setup:**
   ```bash
   cd server
   pip install -r requirements.txt  # Python
   # or
   npm install  # Node.js
   ```
4. **Configure Environment Variables:** Create a `.env` file in the `/server` directory:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/clearbox
   REDIS_URL=redis://localhost:6379
   JWT_SECRET=your_strong_secret_key
   RABBITMQ_URL=amqp://guest:guest@localhost:5672/
   ```
5. **Run the Server:**
   ```bash
   uvicorn main:app --reload  # Python (FastAPI)
   # or
   npm start  # Node.js
   ```
6. **Client Setup (React):**
   ```bash
   cd client
   npm install
   npm run dev
   ```

---

## 📚 API Documentation

### Key Endpoints (FastAPI Example)

| Endpoint            | Method | Description                                 |
|---------------------|--------|---------------------------------------------|
| `/auth/login`       | POST   | User login (returns JWT token)              |
| `/messages/send`    | POST   | Send a message to a user or group           |
| `/messages/history` | GET    | Fetch message history                       |
| `/groups/create`    | POST   | Create a new group                          |
| `/gdpr/delete`      | DELETE | Initiate GDPR data deletion (user/messages) |

**Example Request (Send Message):**

```bash
curl -X POST "http://localhost:8000/messages/send" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiver_id": "123", "content": "Hello, world!"}'
```

### WebSocket Events

- **Connect:** `ws://localhost:8000/ws?token=JWT_TOKEN`
- **Events:**
  - `send_message`: Send a message.
  - `receive_message`: Listen for incoming messages.
  - `user_online`: Update presence status.

---

## 🔒 GDPR Compliance

1. **Data Deletion:** Call `/gdpr/delete` to anonymize user data and messages.  Soft-delete messages initially, then permanently remove after 30 days.
2. **Audit Logs:** All data access is logged in the `audit_logs` table.
3. **Consent Management:** Users must opt-in during registration (stored in `user_consents`).

---

## 🔐 Security Practices

1. **Encryption:** TLS 1.3 for all HTTP/WebSocket traffic.  End-to-end encryption using libsodium.
2. **Authentication:** JWT tokens with 15-minute expiry and refresh tokens.
3. **RBAC:** Admins can delete groups or ban users.

---

## 📈 Scalability

1. **Horizontal Scaling:** Deploy multiple server instances behind an Nginx load balancer.
2. **Database Sharding:** Partition messages by `user_id` or `group_id`.
3. **Caching:** Use Redis to reduce database load for presence checks.

---

## ☁️ Deployment

Deploy to AWS/GCP using:
- ECS/EKS for container orchestration.
- RDS/Cloud SQL for managed databases.
- Cloudflare for TLS and DDoS protection.

Example AWS setup:
```bash
terraform apply
```

---

## 📜 License

MIT License. See [LICENSE](./LICENSE).
