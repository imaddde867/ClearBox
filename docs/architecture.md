# System Architecture

## Overview
The application consists of a client-side UI, a backend server providing REST APIs and WebSocket endpoints, and a message broker for asynchronous message handling.

## Components
- **Client Application:** Built with a framework such as React or Angular.
- **Backend Services:** Microservices for authentication, messaging, and notifications.
- **Message Broker:** To ensure offline messages are queued and delivered.
- **Database:** NoSQL or SQL databases for storing user data and messages.
- **Cloud Infrastructure:** Deployed on AWS/GCP/Azure with container orchestration.

## Diagram
![Architecture Diagram](Plan_Diagram.drawio.png)
