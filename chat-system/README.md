# Chat System

## Overview
This Chat System is a real-time messaging application that allows users to send and receive messages. It utilizes a combination of AWS services, PostgreSQL for data storage, and RabbitMQ for message queuing.

## Features
- Real-time message delivery
- Offline message queuing
- User authentication with AWS Cognito
- Secure storage of credentials using AWS Secrets Manager

## Architecture
The system is built using the following components:
- **AWS VPC**: A Virtual Private Cloud to host the database and other resources.
- **PostgreSQL Database**: For storing user data and messages.
- **RabbitMQ**: For handling message queuing and delivery.
- **AWS Cognito**: For user authentication and management.

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/chat-system.git
   cd chat-system
   ```

2. **Install dependencies**:
   Make sure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory and add the following variables:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://admin:yourpassword@localhost/chatdb
   DB_PASSWORD=yourpassword
   ```

4. **Deploy the infrastructure**:
   Use AWS CDK to deploy the infrastructure:
   ```bash
   cdk deploy
   ```

5. **Run the application**:
   Start the web application:
   ```bash
   python webapp/run.py
   ```

## Usage
- Users can register and log in using their credentials.
- Once logged in, users can send and receive messages in real-time.
- Messages sent while a user is offline will be queued and delivered when they come back online.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
