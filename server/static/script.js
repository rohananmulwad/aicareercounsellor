function toggleChat() {
  const chatWindow = document.getElementById('chatWindow');
  if (chatWindow.style.display === 'flex') {
    chatWindow.style.transform = 'translateY(20px)';
    chatWindow.style.opacity = '0';
    setTimeout(()=> chatWindow.style.display='none', 300);
  } else {
    chatWindow.style.display = 'flex';
    setTimeout(()=>{
      chatWindow.style.transform = 'translateY(0)';
      chatWindow.style.opacity = '1';
    }, 10);
  }
}

function sendMessage() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  if (!message) return;

  const chatMessages = document.getElementById('chatMessages');

  // Add user message
  const userMessage = document.createElement('div');
  userMessage.textContent = message;
  userMessage.style.background = '#58a6ff';
  userMessage.style.color = 'white';
  userMessage.style.padding = '6px 10px';
  userMessage.style.margin = '6px 0';
  userMessage.style.borderRadius = '8px';
  userMessage.style.alignSelf = 'flex-end';
  chatMessages.appendChild(userMessage);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  // Clear input
  input.value = '';

  // Show loading message
  const loadingMessage = document.createElement('div');
  loadingMessage.textContent = 'Loading...';
  loadingMessage.style.fontStyle = 'italic';
  loadingMessage.style.color = '#666';
  chatMessages.appendChild(loadingMessage);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  // Send to Flask backend
  fetch('/aiModel/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
  .then(response => response.text())
  .then(data => {
    chatMessages.removeChild(loadingMessage);

    const botMessage = document.createElement('div');
    botMessage.textContent = data;
    botMessage.style.background = '#f1f3f5';
    botMessage.style.color = '#000';
    botMessage.style.padding = '6px 10px';
    botMessage.style.margin = '6px 0';
    botMessage.style.borderRadius = '8px';
    botMessage.style.alignSelf = 'flex-start';
    chatMessages.appendChild(botMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  })
  .catch(err => {
    chatMessages.removeChild(loadingMessage);
    console.error(err);
  });
}
