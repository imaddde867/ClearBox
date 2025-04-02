

## Key Components Description

1. **Client Layer (CL)**: Web browsers and mobile devices that access the application.

2. **Presentation Layer (PL)**:
   - **Nginx**: Web server handling HTTPS and static file serving
   - **Load Balancing**: Distributes traffic across servers
   - **API Gateway & Proxy**: Routes API requests to appropriate services

3. **Application Layer (AL)**:
   - **Frontend**: React application with components:
     - Auth Context
     - Chat Components
     - MQTT Client
     - Notification
   - **Backend**: FastAPI application with components:
     - Auth Service
     - Message Routes
     - MQTT Service
     - User Management

4. **Messaging Layer (ML)**:
   - **MQTT Broker (Mosquitto)**: Handles:
     - Message Delivery
     - Presence Updates

5. **Data Layer (DL)**:
   - **PostgreSQL Database**: Stores:
     - User Data
     - Messages
     - Conversations

## Data Flow

1. Client Layer connects to Presentation Layer
2. Presentation Layer routes requests to Application Layer
3. Application Layer communicates with Messaging Layer for real-time updates
4. Messaging Layer interacts with Data Layer for persistent storage