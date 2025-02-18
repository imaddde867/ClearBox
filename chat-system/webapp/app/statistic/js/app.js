document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const messageInput = document.getElementById('message-text');
    const sendButton = document.getElementById('send-message');
    const messagesContainer = document.querySelector('.messages-container');

    socket.on('connect', function() {
        console.log('Connected to server');
    });

    socket.on('message', function(data) {
        appendMessage(data);
    });

    sendButton.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            socket.emit('send_message', {
                content: message,
                recipient_id: currentChatId  // Global variable set when selecting a chat
            });
            messageInput.value = '';
        }
    });

    function appendMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.textContent = `${message.sender}: ${message.content}`;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});