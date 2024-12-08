document.addEventListener('DOMContentLoaded', () => {
    window.debugStorage = {
        clearProfile: function() {
            localStorage.removeItem('userProfile');
            localStorage.removeItem('conversations');
            console.log('Profile and conversations cleared');
            window.location.reload();
        }
    };

    const userProfileForm = document.getElementById('user-profile-form');
    const onboardingForm = document.getElementById('onboarding-form');
    const chatInterface = document.getElementById('chat-interface');

    // Check if user profile exists
    const userProfile = localStorage.getItem('userProfile');
    if (userProfile) {
        console.log('Loading profile:', JSON.parse(userProfile)); // Debug log
        showChatInterface();
    }

    // Handle form submission
    userProfileForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get selected emotions (multiple select)
        const emotionsSelect = document.getElementById('emotions');
        const selectedEmotions = Array.from(emotionsSelect.selectedOptions).map(option => option.value);
        
        const profile = {
            name: document.getElementById('name').value,
            age: document.getElementById('age').value,
            emotions: selectedEmotions,
            therapyStatus: document.getElementById('therapy-status').value,
            interactionStyle: document.getElementById('interaction-style').value,
            stressLevel: document.getElementById('stress-level').value,
            goals: document.getElementById('goals').value,
            createdAt: new Date().toISOString()
        };

        // Debug log before saving
        console.log('Saving profile:', profile);
        localStorage.setItem('userProfile', JSON.stringify(profile));
        showChatInterface();
    });

    function showChatInterface() {
        onboardingForm.classList.add('hidden');
        chatInterface.classList.remove('hidden');
        initializeChatInterface();
    }

    function initializeChatInterface() {
        const userMessage = document.getElementById('user-message');
        const sendButton = document.getElementById('send-button');
        const conversationHistory = document.getElementById('conversation-history');

        // Load previous conversations
        loadConversations();

        // Style updates for chat interface
        chatInterface.style.display = 'flex';
        chatInterface.style.flexDirection = 'column';
        chatInterface.style.height = '100vh';
        
        // Style the conversation history
        conversationHistory.style.flex = '1';
        conversationHistory.style.overflowY = 'auto';
        conversationHistory.style.padding = '20px';
        
        // Create a container for the input area
        const inputContainer = document.createElement('div');
        inputContainer.style.padding = '20px';
        inputContainer.style.borderTop = '1px solid #eee';
        inputContainer.style.backgroundColor = '#fff';
        
        // // Style the textarea
        // userMessage.style.width = '100%';
        // userMessage.style.padding = '10px';
        // userMessage.style.border = '1px solid #ddd';
        // userMessage.style.borderRadius = '4px';
        // userMessage.style.marginBottom = '10px';
        // userMessage.style.resize = 'none';
        // userMessage.placeholder = 'Enter your message...';
        
        // // Style the send button
        // sendButton.className = 'btn btn-primary';
        // sendButton.style.padding = '8px 24px';
        // sendButton.style.backgroundColor = '#3498db';
        // sendButton.style.border = 'none';
        // sendButton.style.borderRadius = '4px';
        // sendButton.style.color = '#fff';
        // sendButton.style.cursor = 'pointer';
        
        // Move elements to input container
        inputContainer.appendChild(userMessage);
        inputContainer.appendChild(sendButton);
        chatInterface.appendChild(inputContainer);

        sendButton.addEventListener('click', async () => {
            const message = userMessage.value.trim();
            if (message) {
                // Save and display message
                saveConversation(message, 'user');
                displayMessage(message, 'user');
                userMessage.value = '';

                // Get AI response
                const response = await getAIResponse(message);
                saveConversation(response, 'ai');
                displayMessage(response, 'ai');
            }
        });

        // Add header controls
        const headerControls = document.createElement('div');
        headerControls.className = 'header-controls';
        
        // Add theme toggle
        const themeToggle = document.createElement('label');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = `
            <input type="checkbox" id="theme-switch">
            <span class="toggle-slider"></span>
        `;
        
        // Add new chat button
        const newChatBtn = document.createElement('button');
        newChatBtn.className = 'new-chat-btn';
        newChatBtn.textContent = '+ Create new chat';
        
        headerControls.appendChild(themeToggle);
        headerControls.appendChild(newChatBtn);
        
        // Insert header at the top of chat interface
        chatInterface.insertBefore(headerControls, chatInterface.firstChild);
        
        // Theme toggle functionality
        const themeSwitch = document.getElementById('theme-switch');
        themeSwitch.addEventListener('change', () => {
            document.body.classList.toggle('dark-theme');
            // Save theme preference
            localStorage.setItem('theme', themeSwitch.checked ? 'dark' : 'light');
        });
        
        // New chat functionality
        newChatBtn.addEventListener('click', () => {
            // Clear conversation history
            conversationHistory.innerHTML = '';
            // Clear localStorage conversations
            localStorage.setItem('conversations', '[]');
            // Optional: Add a welcome message
            displayMessage("How can I help you today?", 'ai');
        });

        // Load saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            themeSwitch.checked = savedTheme === 'dark';
            document.body.classList.toggle('dark-theme', savedTheme === 'dark');
        }
    }

    function saveConversation(message, sender) {
        const conversations = JSON.parse(localStorage.getItem('conversations') || '[]');
        conversations.push({
            message,
            sender,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('conversations', JSON.stringify(conversations));
    }

    function loadConversations() {
        const conversations = JSON.parse(localStorage.getItem('conversations') || '[]');
        conversations.forEach(conv => {
            displayMessage(conv.message, conv.sender);
        });
    }

    function displayMessage(message, sender) {
        const conversationHistory = document.getElementById('conversation-history');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.innerHTML = `<strong>${sender === 'user' ? 'You' : 'AI'}:</strong> ${message}`;
        conversationHistory.appendChild(messageElement);
        conversationHistory.scrollTop = conversationHistory.scrollHeight;
    }

    async function getAIResponse(message) {
        // Placeholder for AI model integration
        return "This is a placeholder response. Integrate with your LLM model here.";
    }

    function initializeMoodSelector() {
        const moodSelector = document.querySelector('.mood-selector');
        const userMessage = document.getElementById('user-message');
        const sendButton = document.getElementById('send-button');

        sendButton.addEventListener('click', () => {
            const message = userMessage.value;
            const mood = moodSelector.value;
            if (message && mood) {
                // Send both message and mood to your chat handler
                handleChat(message, mood);
            }
        });
    }

    function handleChat(message, mood) {
        // Include mood in the context when sending to the AI
        const context = {
            message: message,
            userMood: mood
        };
        // Your existing chat handling logic here
    }
});