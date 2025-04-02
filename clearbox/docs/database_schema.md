# ClearBox Database Schema

```
┌─────────────────────────┐       ┌─────────────────────────┐
│         users           │       │      conversations      │
├─────────────────────────┤       ├─────────────────────────┤
│ id: UUID (PK)           │       │ id: UUID (PK)           │
│ email: VARCHAR          │◄──┐   │ name: VARCHAR           │
│ name: VARCHAR           │   │   │ created_at: TIMESTAMP   │
│ password: VARCHAR       │   │   │ updated_at: TIMESTAMP   │
│ avatar: VARCHAR         │   │   │ is_group: BOOLEAN       │
│ bio: TEXT               │   │   │ owner_id: UUID (FK)     │────┐
│ status: VARCHAR         │   │   └─────────────────────────┘    │
│ last_seen: TIMESTAMP    │   │                                  │
│ created_at: TIMESTAMP   │   │                                  │
│ updated_at: TIMESTAMP   │   │                                  │
└─────────────────────────┘   │                                  │
                              │                                  │
┌─────────────────────────┐   │   ┌─────────────────────────┐   │
│  conversation_members   │   │   │        messages         │   │
├─────────────────────────┤   │   ├─────────────────────────┤   │
│ id: UUID (PK)           │   │   │ id: UUID (PK)           │   │
│ conversation_id: UUID(FK)│───┘   │ conversation_id: UUID(FK)│───┘
│ user_id: UUID (FK)      │◄──────┐│ sender_id: UUID (FK)    │
│ joined_at: TIMESTAMP    │       ││ content: TEXT           │
│ nickname: VARCHAR       │       ││ created_at: TIMESTAMP   │
│ role: VARCHAR           │       ││ updated_at: TIMESTAMP   │
└─────────────────────────┘       ││ read: BOOLEAN          │
                                  ││ encrypted: BOOLEAN      │
┌─────────────────────────┐       │└─────────────────────────┘
│      user_contacts      │       │
├─────────────────────────┤       │
│ id: UUID (PK)           │       │          
│ user_id: UUID (FK)      │───────┘          
│ contact_id: UUID (FK)   │◄──────┐           
│ created_at: TIMESTAMP   │       │         
│ nickname: VARCHAR       │       │       
│ status: VARCHAR         │       │      
└─────────────────────────┘       │       
                                  │
┌─────────────────────────┐       │
│      notifications      │       │
├─────────────────────────┤       │
│ id: UUID (PK)           │       │
│ user_id: UUID (FK)      │───────┘
│ type: VARCHAR           │
│ content: TEXT           │
│ read: BOOLEAN           │
│ created_at: TIMESTAMP   │
│ reference_id: UUID      │
└─────────────────────────┘

```

## Schema Description

### Users Table
- Primary storage for user accounts 
- Contains authentication credentials (hashed passwords)
- Tracks user status and last activity time

### Conversations Table
- Represents chat conversations (1-on-1 or group)
- Owner references the user who created the conversation
- Groups are distinguished by the is_group flag

### Conversation Members Table
- Junction table connecting users to conversations
- Tracks when a user joined a conversation
- Stores user-specific settings like nicknames and roles

### Messages Table
- Stores all messages sent in conversations
- Tracks read status for message receipts
- Content is encrypted using the encryption key

### User Contacts Table
- Manages user's contact list
- Allows custom nicknames for contacts
- Tracks contact relationship status (pending, accepted, blocked)

### Notifications Table
- Stores system notifications for users
- Different notification types (message, contact request, etc.)
- Reference ID can point to related entities

## Security Considerations

- Passwords are hashed with bcrypt
- Message content is encrypted with Fernet symmetric encryption
- Database connections use TLS/SSL
- Database queries use parameterized statements to prevent SQL injection 