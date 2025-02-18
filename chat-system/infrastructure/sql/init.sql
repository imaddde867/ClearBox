-- Defining the database schema:

-- Table for users
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMPTZ,
    data_processing_consent TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB
);

-- Table for groups
CREATE TABLE groups (
    group_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_name VARCHAR(250) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    owner_id UUID REFERENCES users(user_id) ON DELETE CASCADE NOT NULL,  
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB
);

-- Table for group members
CREATE TABLE group_members (
    group_id UUID REFERENCES groups(group_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    joined_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(50) DEFAULT 'member',
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB,
    PRIMARY KEY (group_id, user_id)
);

-- Table for messages
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id UUID REFERENCES users(user_id) ON DELETE CASCADE,  
    recipient_id UUID REFERENCES users(user_id) ON DELETE CASCADE,  
    group_id UUID REFERENCES groups(group_id) ON DELETE CASCADE, 
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ, -- for GDPRR compliance
    metadata JSONB
);

-- Table for offline messages
CREATE TABLE offline_messages (
    offline_message_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id UUID REFERENCES messages(message_id) ON DELETE CASCADE,
    recipient_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    message_content TEXT, 
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMPTZ,
    delivery_attempts INT DEFAULT 0,
    metadata JSONB,
    UNIQUE (message_id, recipient_id)
);

-- Function to queue offline messages
CREATE OR REPLACE FUNCTION queue_offline_message(message_id UUID, recipient_id UUID)
RETURNS VOID AS $$
DECLARE
    message_content TEXT;
    message_metadata JSONB;
BEGIN
    SELECT content, metadata INTO message_content, message_metadata
    FROM messages
    WHERE message_id = $1;

    INSERT INTO offline_messages(message_id, recipient_id, created_at, message_content, metadata)
    VALUES ($1, $2, NOW(), message_content, message_metadata)
    ON CONFLICT (message_id, recipient_id) DO NOTHING;

    PERFORM pg_notify('message_queue', json_build_object(
        'message_id', $1,
        'recipient_id', $2,
        'content', message_content,
        'metadata', message_metadata
    )::text);
END;
$$ LANGUAGE plpgsql;

-- Trigger to handle new messages
CREATE OR REPLACE FUNCTION handle_new_message()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.recipient_id IS NOT NULL THEN
        PERFORM queue_offline_message(NEW.message_id, NEW.recipient_id);
    ELSIF NEW.group_id IS NOT NULL THEN
        INSERT INTO offline_messages (message_id, recipient_id, created_at)
        SELECT NEW.message_id, user_id, NOW()
        FROM group_members
        WHERE group_id = NEW.group_id
        AND user_id != NEW.sender_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;