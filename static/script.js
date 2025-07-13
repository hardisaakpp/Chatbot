// static/script.js
function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    const chatBox = document.getElementById('chat-box');
    const userMessage = document.createElement('p');
    userMessage.className = 'message user-message';
    userMessage.innerHTML = `${userInput}`;
    chatBox.appendChild(userMessage);

    fetch('/get_response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `user_input=${encodeURIComponent(userInput)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            chatBox.innerHTML += `<p class="message bot-message"><strong>Error:</strong> ${data.error}</p>`;
        } else {
            typeResponse(data.response);
        }
        document.getElementById('user-input').value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        chatBox.innerHTML += `<p class="message bot-message"><strong>Error:</strong> ${error.message}</p>`;
    });
}

function typeResponse(response) {
    const chatBox = document.getElementById('chat-box');
    const responseElement = document.createElement('p');
    responseElement.className = 'message bot-message';
    responseElement.innerHTML = `<strong>Chatbot:</strong> `;
    chatBox.appendChild(responseElement);

    let i = 0;
    function type() {
        if (i < response.length) {
            responseElement.innerHTML += response.charAt(i);
            i++;
            setTimeout(type, 20); // Adjust typing speed here
        }
    }
    type();
}

// Add event listener for Enter key
document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});