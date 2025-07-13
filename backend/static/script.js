// static/script.js
// Variables globales
let messageCount = 0;
let isTyping = false;

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    updateMessageCounter();
    setupEventListeners();
    scrollToBottom();
});

// Configurar event listeners
function setupEventListeners() {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // Enviar mensaje con Enter
    userInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // Enviar mensaje con botón
    sendButton.addEventListener('click', sendMessage);
    
    // Auto-resize del input (para futuras mejoras)
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
    
    // Focus en el input al cargar
    userInput.focus();
}

// Función principal para enviar mensaje
function sendMessage() {
    const userInput = document.getElementById('user-input');
    const userMessage = userInput.value.trim();
    
    if (userMessage === '' || isTyping) return;
    
    // Agregar mensaje del usuario
    addUserMessage(userMessage);
    
    // Limpiar input y deshabilitar botón
    userInput.value = '';
    userInput.style.height = 'auto';
    setSendButtonState(false);
    
    // Mostrar indicador de escritura
    showTypingIndicator();
    
    // Enviar petición al servidor
    fetch('/get_response', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: `user_input=${encodeURIComponent(userMessage)}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        hideTypingIndicator();
        if (data.error) {
            addBotMessage(`❌ Error: ${data.error}`, 'error');
        } else {
            typeResponse(data.response);
        }
        setSendButtonState(true);
    })
    .catch(error => {
        hideTypingIndicator();
        addBotMessage(`❌ Error de conexión: ${error.message}`, 'error');
        setSendButtonState(true);
        console.error('Error:', error);
    });
}

// Agregar mensaje del usuario
function addUserMessage(message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    const timestamp = getCurrentTimestamp();
    
    messageElement.className = 'message user-message';
    messageElement.innerHTML = `
        ${escapeHtml(message)}
        <span class="timestamp">${timestamp}</span>
    `;
    
    chatBox.appendChild(messageElement);
    messageCount++;
    updateMessageCounter();
    scrollToBottom();
}

// Agregar mensaje del bot
function addBotMessage(message, type = 'normal') {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    const timestamp = getCurrentTimestamp();
    
    messageElement.className = `message bot-message ${type}`;
    messageElement.innerHTML = `
        ${escapeHtml(message)}
        <span class="timestamp">${timestamp}</span>
    `;
    
    chatBox.appendChild(messageElement);
    messageCount++;
    updateMessageCounter();
    scrollToBottom();
}

// Efecto de escritura para respuestas del bot
function typeResponse(response) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    const timestamp = getCurrentTimestamp();
    
    messageElement.className = 'message bot-message';
    messageElement.innerHTML = `
        <span class="response-text"></span>
        <span class="timestamp">${timestamp}</span>
    `;
    
    chatBox.appendChild(messageElement);
    messageCount++;
    updateMessageCounter();
    
    const responseText = messageElement.querySelector('.response-text');
    let i = 0;
    const typingSpeed = 30; // milisegundos por carácter
    
    function typeChar() {
        if (i < response.length) {
            responseText.innerHTML += response.charAt(i);
            i++;
            scrollToBottom();
            setTimeout(typeChar, typingSpeed);
        } else {
            // Agregar cursor parpadeante al final
            responseText.innerHTML += '<span class="typing-cursor">|</span>';
            setTimeout(() => {
                const cursor = responseText.querySelector('.typing-cursor');
                if (cursor) cursor.remove();
            }, 1000);
        }
    }
    
    typeChar();
}

// Mostrar indicador de escritura
function showTypingIndicator() {
    const chatBox = document.getElementById('chat-box');
    const typingElement = document.createElement('div');
    typingElement.className = 'typing-indicator';
    typingElement.id = 'typing-indicator';
    typingElement.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    
    chatBox.appendChild(typingElement);
    isTyping = true;
    scrollToBottom();
}

// Ocultar indicador de escritura
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
    isTyping = false;
}

// Función para preguntas rápidas
function askQuestion(question) {
    const userInput = document.getElementById('user-input');
    userInput.value = question;
    sendMessage();
}

// Limpiar chat
function clearChat() {
    if (confirm('¿Estás seguro de que quieres limpiar todo el historial del chat?')) {
        const chatBox = document.getElementById('chat-box');
        
        // Mantener solo el mensaje de bienvenida
        const welcomeMessage = chatBox.querySelector('.welcome-message');
        chatBox.innerHTML = '';
        if (welcomeMessage) {
            chatBox.appendChild(welcomeMessage);
        }
        
        // Resetear contador
        messageCount = 0;
        updateMessageCounter();
        
        // Mostrar mensaje de confirmación
        setTimeout(() => {
            addBotMessage('✅ Historial del chat limpiado correctamente.', 'success');
        }, 300);
    }
}

// Actualizar contador de mensajes
function updateMessageCounter() {
    const counter = document.getElementById('message-count');
    if (counter) {
        counter.textContent = messageCount;
    }
}

// Obtener timestamp actual
function getCurrentTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Scroll automático al final
function scrollToBottom() {
    const chatBox = document.getElementById('chat-box');
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 100);
}

// Cambiar estado del botón de envío
function setSendButtonState(enabled) {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    
    if (enabled) {
        sendButton.disabled = false;
        userInput.disabled = false;
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
    } else {
        sendButton.disabled = true;
        userInput.disabled = true;
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }
}

// Escapar HTML para prevenir XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Efectos visuales adicionales
function addVisualEffects() {
    // Efecto de hover en mensajes
    document.addEventListener('mouseover', function(e) {
        if (e.target.classList.contains('message')) {
            e.target.style.transform = 'translateY(-2px)';
        }
    });
    
    document.addEventListener('mouseout', function(e) {
        if (e.target.classList.contains('message')) {
            e.target.style.transform = 'translateY(0)';
        }
    });
}

// Inicializar efectos visuales
addVisualEffects();

// Función para guardar historial en localStorage (opcional)
function saveChatHistory() {
    const chatBox = document.getElementById('chat-box');
    const messages = Array.from(chatBox.querySelectorAll('.message')).map(msg => ({
        text: msg.textContent,
        type: msg.classList.contains('user-message') ? 'user' : 'bot',
        timestamp: msg.querySelector('.timestamp')?.textContent
    }));
    
    localStorage.setItem('chatHistory', JSON.stringify(messages));
}

// Función para cargar historial desde localStorage (opcional)
function loadChatHistory() {
    const savedHistory = localStorage.getItem('chatHistory');
    if (savedHistory) {
        const messages = JSON.parse(savedHistory);
        messages.forEach(msg => {
            if (msg.type === 'user') {
                addUserMessage(msg.text);
            } else {
                addBotMessage(msg.text);
            }
        });
    }
}

// Auto-guardar cada 10 mensajes
setInterval(() => {
    if (messageCount > 0 && messageCount % 10 === 0) {
        saveChatHistory();
    }
}, 1000);