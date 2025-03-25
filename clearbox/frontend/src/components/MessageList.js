import React, { useEffect, useRef, useState } from 'react';

const MessageList = ({ messages, currentUser }) => {
  const messagesEndRef = useRef(null);
  const messageListRef = useRef(null);
  const [shouldAutoScroll, setShouldAutoScroll] = useState(true);
  const lastMessageCountRef = useRef(0);

  // Auto scroll to bottom when messages change
  useEffect(() => {
    if (!messages || !messages.length) return;

    const currentMessageCount = messages.length;
    const newMessagesAdded = currentMessageCount > lastMessageCountRef.current;

    // Check if user was already scrolled to bottom (or close to it) before new message
    const isScrolledToBottom = () => {
      if (!messageListRef.current) return true;

      const { scrollTop, scrollHeight, clientHeight } = messageListRef.current;
      // Consider "close to bottom" as within 100px of the bottom
      return scrollHeight - scrollTop - clientHeight < 100;
    };

    // When we receive new messages
    if (newMessagesAdded) {
      // If user was already at bottom, or it's our own message, scroll to bottom
      const lastMessage = messages[messages.length - 1] || {};
      const isOwnMessage = lastMessage.sender_id === currentUser?.id;

      if (shouldAutoScroll || isOwnMessage || isScrolledToBottom()) {
        setTimeout(() => {
          messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      }
    }

    // Update message count reference
    lastMessageCountRef.current = currentMessageCount;
  }, [messages, currentUser, shouldAutoScroll]);

  // Set up scroll listener to determine if auto-scroll should be enabled
  useEffect(() => {
    const handleScroll = () => {
      if (!messageListRef.current) return;

      const { scrollTop, scrollHeight, clientHeight } = messageListRef.current;
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;

      setShouldAutoScroll(isNearBottom);
    };

    const messageList = messageListRef.current;
    if (messageList) {
      messageList.addEventListener('scroll', handleScroll);
    }

    return () => {
      if (messageList) {
        messageList.removeEventListener('scroll', handleScroll);
      }
    };
  }, []);

  // Initial scroll to bottom when component mounts
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView();
  }, []);

  return (
    <div className="message-list-container" ref={messageListRef}>
      {messages && messages.length > 0 ? (
        <>
          {messages.map((message) => (
            <Message
              key={message.id}
              message={message}
              isOwnMessage={message.sender_id === currentUser?.id}
            />
          ))}
          <div ref={messagesEndRef} />
        </>
      ) : (
        <div className="no-messages">
          <p>No messages yet. Start the conversation!</p>
        </div>
      )}
    </div>
  );
};

export default MessageList;