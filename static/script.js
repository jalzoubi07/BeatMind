let conversationHistory = [];

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    addMessage(message, 'user');
    input.value = '';
    
    conversationHistory.push({
        role: 'user',
        content: message
    });
    
    addMessage('BeatMind is thinking...', 'beatmind', 'typing');
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                message: message,
                history: conversationHistory.slice(0, -1)
            })
        });
        
        const data = await response.json();
        
        removeTyping();
        
        addMessage(data.response, 'beatmind');
        
        conversationHistory.push({
            role: 'assistant',
            content: data.response
        });
        
    } catch (error) {
        removeTyping();
        addMessage('Something went wrong. Try again.', 'beatmind');
    }
}

function addMessage(text, sender, id = '') {
    const chatWindow = document.getElementById('chat-window');
    const message = document.createElement('div');
    message.className = `message ${sender}`;
    if (id) message.id = id;
    message.textContent = text;
    chatWindow.appendChild(message);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById('typing');
    if (typing) typing.remove();
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}