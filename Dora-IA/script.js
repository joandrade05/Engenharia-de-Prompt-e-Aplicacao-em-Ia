// ================================
// DORA - Emotional Monitoring AI
// Navigation & Interactivity
// ================================

// Get all navigation items and sections
const navItems = document.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('.section');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const chatMessages = document.querySelector('.chat-messages');

// Sample responses from Dora AI
const doraResponses = {
    greeting: [
        'Que bom te ver! Como você está se sentindo hoje?',
        'Olá! Estou aqui para te ouvir. O que está em sua mente?',
        'Oi! Vamos conversar sobre seus sentimentos?'
    ],
    positive: [
        'Que alegria! É incrível ouvir isso! 😊',
        'Que maravilhoso! Continue assim!',
        'Adorei ouvir isso! Você está brilhando! ✨'
    ],
    negative: [
        'Entendo que você está passando por isso. Quer falar mais sobre?',
        'Estou aqui para ajudar. Todos temos dias difíceis.',
        'Obrigada por compartilhar. Vamos trabalhar juntas nisto.'
    ],
    anxiety: [
        'A ansiedade é comum. Que tal tentarmos uma técnica de respiração?',
        'Eu sinto que você está um pouco ansioso. Posso ajudar com algumas estratégias.',
        'Tudo bem sentir-se assim. Vamos encontrar maneiras de acalmar.'
    ],
    gratitude: [
        'De nada! Estou aqui sempre que precisar! 💜',
        'Fico feliz em poder ajudar!',
        'Você é incrível! Continue tomando conta de você!'
    ]
};

// ================================
// EVENT LISTENERS
// ================================

// Navigation switching
navItems.forEach(item => {
    item.addEventListener('click', () => {
        // Remove active class from all items
        navItems.forEach(nav => nav.classList.remove('active'));
        sections.forEach(section => section.classList.remove('active'));

        // Add active class to clicked item
        item.classList.add('active');
        const sectionId = `${item.dataset.section}-section`;
        const section = document.getElementById(sectionId);
        
        if (section) {
            section.classList.add('active');
        }
    });
});

// Chat form submission
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    
    if (message === '') return;

    // Add user message
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    messageInput.focus();

    // Simulate Dora's response with delay
    setTimeout(() => {
        const response = generateDoraResponse(message);
        addMessage(response, 'dora');
    }, 500 + Math.random() * 1000);
});

// ================================
// FUNCTIONS
// ================================

/**
 * Add a message to the chat
 * @param {string} message - The message text
 * @param {string} sender - 'user' or 'dora'
 */
function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const timestamp = new Date().toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
    });

    if (sender === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${escapeHtml(message)}</p>
                <span class="timestamp">${timestamp}</span>
            </div>
            <div class="message-avatar">👤</div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <p>${message}</p>
                <span class="timestamp">Agora</span>
            </div>
        `;
    }

    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Generate a response from Dora based on user message
 * @param {string} message - User message
 * @returns {string} - Dora's response
 */
function generateDoraResponse(message) {
    const lowerMessage = message.toLowerCase();

    // Detect emotion and respond accordingly
    if (
        lowerMessage.includes('obrigado') ||
        lowerMessage.includes('obrigada') ||
        lowerMessage.includes('valeu')
    ) {
        return getRandomResponse(doraResponses.gratitude);
    }

    if (
        lowerMessage.includes('ansiedade') ||
        lowerMessage.includes('ansioso') ||
        lowerMessage.includes('preocupado') ||
        lowerMessage.includes('assustado')
    ) {
        return getRandomResponse(doraResponses.anxiety);
    }

    if (
        lowerMessage.includes('feliz') ||
        lowerMessage.includes('alegre') ||
        lowerMessage.includes('bem') ||
        lowerMessage.includes('ótimo') ||
        lowerMessage.includes('excelente')
    ) {
        return getRandomResponse(doraResponses.positive);
    }

    if (
        lowerMessage.includes('triste') ||
        lowerMessage.includes('mal') ||
        lowerMessage.includes('ruim') ||
        lowerMessage.includes('deprimido') ||
        lowerMessage.includes('infeliz')
    ) {
        return getRandomResponse(doraResponses.negative);
    }

    // Default response
    return getRandomResponse([
        'Entendi! Pode me contar mais sobre isso?',
        'Interessante! Como você se sente com relação a isso?',
        'Que perspectiva interessante. Qual é o contexto?',
        'Ótimo! Vamos conversar mais sobre isso.'
    ]);
}

/**
 * Get a random response from an array
 * @param {array} responseArray - Array of responses
 * @returns {string} - Random response
 */
function getRandomResponse(responseArray) {
    return responseArray[Math.floor(Math.random() * responseArray.length)];
}

/**
 * Escape HTML special characters
 * @param {string} text - Text to escape
 * @returns {string} - Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ================================
// INITIALIZATION
// ================================

/**
 * Initialize the application
 */
function initialize() {
    console.log('Dora AI Initialized ✨');
    
    // Show welcome message
    addMessage(doraResponses.greeting[0], 'dora');
    
    // Add keyboard shortcut info
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to send message
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (document.activeElement === messageInput) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initialize);

// ================================
// ADDITIONAL INTERACTIVITY
// ================================

// Add smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';

// Track user focus for engagement
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('Dora paused - tab not active');
    } else {
        console.log('Dora resumed - welcome back!');
    }
});

// Prevent empty messages
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Add active state to navigation on page load
window.addEventListener('load', () => {
    console.log('Dora AI fully loaded and ready!');
});
