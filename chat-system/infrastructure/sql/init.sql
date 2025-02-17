-- defining the database scheme:

--first table for users :
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), --uuid usually includes 122 bits of cryptographically strong randomness much more secure than sequential IDs
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, --USES TIMEZONE-AWARE TIMESTAMPS FORR ACCURATE TIMING ACCROSS DIFFERENT REGIONS
    last_seen TIMESTAMPTZ,
    data_processing_consent TIMESTAMPTZ, --to comply with GDPR by tracking consent
    is_active BOOLEAN DEFAULT true,
    metadata JSONB --to allow flexible storage of additional user data
);

--second table for groups :
CREATE TABLE groups (
    group_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_name VARCHAR(250) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    owner_id UUID REFERENCES users(user_id) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB
);

--third table for group members with a many to many relationship between users and groups :
CREATE TABLE group_members (
        group_id UUID REFERENCES groups(group_id) ON DELETE CASCADE,
        user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
        joined_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        role VARCHAR(50) DEFAULT 'member',
        is_active BOOLEAN DEFAULT true,
        metadata JSONB,
        PRIMARY KEY (group_id, user_id)
    );

--fourth table for messages :
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id UUID REFERENCES users(user_id),
    recipient_id UUID REFERENCES users(user_id) NULL,
    group_id UUID REFERENCES groups(group_id) NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,  -- to comply with GDPR message retention
    metadata JSONB,
    CHECK (
        (recipient_id IS NOT NULL AND group_id IS NULL) OR
        (recipient_id IS NULL AND group_id IS NOT NULL)
    )
);

--table for storing offline messages that need to be delivered when recipients come online:
CREATE TABLE offline_messages (
    offline_message_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id UUID REFERENCES messages(message_id) ON DELETE CASCADE,
    recipient_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMPTZ,
    delivery_attempts INT DEFAULT 0,
    metadata JSONB,
    UNIQUE(message_id, recipient_id)
);

CREATE OR REPLACE FUNCTION queue_offline_message(message_id UUID, recipient_id UUID)
RETURNS VOID AS $$
DECLARE
    message_content TEXT;
    message_metadata JSONB;
BEGIN
    SELECT content, metadata INTO message_content, message_metadata
    FROM messages
    WHERE message_id = queue_offline_message.message_id;

    --now we insert it into offline_messages
    INSERT INTO offline_messages(message_id, recipient_id, created_at, metadata)
    VALUES (message_id, recipient_id, NOW(), message_metadata)
    ON CONFLICT (message_id, recipient_id) DO NOTHING;

    --publish to RabbitMQ
    PERFORM pg_notify('message_queue', json_build_object(
        'message_id', message_id,
        'recipient_id', recipient_id,
        'content', message_content,
        'metadata', message_metadata
    )::text);
END;
$$ LANGUAGE plpgsql;

-- defining a trigger function that handles message delivery logic whenever a new message is inserted into the messages table above.
CREATE OR REPLACE FUNCTION handle_new_message()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.recipient_id IS NOT NULL THEN
        PERFORM queue_offline_message(NEW.message_id, NEW.recipient_id);
    ELSIF NEW.group_id IS NOT NULL THEN
        INSERT INTO offline_messages (message_id, recipient_id)
        SELECT NEW.message_id, user_id
        FROM group_members
        WHERE group_id = NEW.group_id
        AND user_id != NEW.sender_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;