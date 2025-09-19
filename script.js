document.addEventListener('DOMContentLoaded', function() {
    // Set active sidebar item based on current page
    const currentPage = window.location.pathname.split('/').pop().split('.')[0];
    document.querySelectorAll('.sidebar-item').forEach(item => {
        if (item.getAttribute('onclick').includes(currentPage)) {
            item.classList.add('active');
        }
    });

    // Initialize chat widget
    const chatToggle = document.querySelector('.chat-toggle');
    if (chatToggle) {
        chatToggle.addEventListener('click', toggleChat);
    }

    // Initialize mobile menu
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', toggleSidebar);
    }
});

// Navigation Functions
function navigateTo(page) {
    const routes = {
        'dashboard': 'dashboard.html',
        'assessment': 'quiz.html',
        'careers': 'explore-courses.html',
        'skills': 'skill-advisor.html',
        'roadmap': 'career-roadmap.html',
        'chat': 'ai-coach.html',
        'settings': 'settings.html',
        'help': 'help.html'
    };

    if (routes[page]) {
        window.location.href = routes[page];
    }
}

// Sidebar Toggle
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
}

// Quick Actions
function resumeAssessment() {
    const lastAssessment = localStorage.getItem('lastAssessment');
    if (lastAssessment) {
        navigateTo('assessment');
    } else {
        alert('No previous assessment found. Start a new one!');
    }
}

function viewRecommendations() {
    // Implement news and updates functionality
    alert('Loading latest news and updates...');
    // You can replace this with actual news feed implementation
}

function scheduleCall() {
    // Implement consultation scheduling
    const consultationForm = `
        <h3>Schedule a Consultation</h3>
        <form id="consultationForm">
            <input type="date" required>
            <input type="time" required>
            <button type="submit">Confirm</button>
        </form>
    `;
    alert('Opening scheduling calendar...');
    // Implement actual scheduling functionality
}

// Profile and Notifications
function showNotifications() {
    const notifications = [
        'New career opportunity matching your profile',
        'Quiz results are ready',
        'New skill recommendation available'
    ];
    
    alert('Recent Notifications:\n\n' + notifications.join('\n'));
    // Replace with proper notifications panel
}

function openProfile() {
    navigateTo('profile');
    // Implement profile page navigation
}

// Chat Widget Functions
function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'block' : 'none';
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (message) {
        const messagesDiv = document.querySelector('.chat-messages');
        
        // Add user message
        const userMessage = document.createElement('div');
        userMessage.className = 'user-message';
        userMessage.textContent = message;
        messagesDiv.appendChild(userMessage);
        
        // Clear input
        input.value = '';
        
        // Simulate AI response
        setTimeout(() => {
            const botMessage = document.createElement('div');
            botMessage.className = 'bot-message';
            botMessage.textContent = "I understand you're asking about " + message + ". Let me help you with that.";
            messagesDiv.appendChild(botMessage);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }, 1000);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Set active sidebar item based on current page
    const currentPage = window.location.pathname.split('/').pop().split('.')[0];
    document.querySelectorAll('.sidebar-item').forEach(item => {
        const onclick = item.getAttribute('onclick');
        if (onclick && onclick.includes(currentPage)) {
            item.classList.add('active');
        }
    });

    // Initialize chat input event listener
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Feature card hover effects
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
});

// Progress tracking for quiz/assessment
function updateProgress(value) {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = `${value}%`;
    }
}

// Helper function for loading states
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const originalContent = element.innerHTML;
        element.innerHTML = 'Loading...';
        return () => element.innerHTML = originalContent;
    }
    return () => {};
}
