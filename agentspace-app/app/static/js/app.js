/**
 * HippoLingua Application JavaScript
 */

// DOM Elements
const audioElement = document.getElementById('audio-element');
const audioTitle = document.getElementById('audio-title');
const audioDescription = document.getElementById('audio-description');
const speedControl = document.getElementById('speed-control');
const speedValue = document.getElementById('speed-value');
const audioList = document.getElementById('audio-list');
const searchInput = document.getElementById('search-input');
const languageFilter = document.getElementById('language-filter');
const contentFilter = document.getElementById('content-filter');
const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Audio player functionality
speedControl.addEventListener('input', function() {
    const speed = parseFloat(this.value);
    audioElement.playbackRate = speed;
    speedValue.textContent = `${speed.toFixed(1)}x`;
});

// Play button functionality
document.querySelectorAll('.play-button').forEach(button => {
    button.addEventListener('click', function() {
        const audioId = this.getAttribute('data-id');
        playAudio(audioId);
    });
});

/**
 * Play audio file by ID
 * @param {string} audioId - ID of the audio file
 * @param {Object} options - Playback options
 */
function playAudio(audioId, options = {}) {
    const defaultOptions = {
        startTime: 0,
        endTime: null,
        speed: 1.0,
        repeat: false
    };
    
    const playbackOptions = { ...defaultOptions, ...options };
    
    // Build URL with query parameters
    let url = `/api/audio/${audioId}/play?start_time=${playbackOptions.startTime}&speed=${playbackOptions.speed}`;
    
    if (playbackOptions.endTime) {
        url += `&end_time=${playbackOptions.endTime}`;
    }
    
    if (playbackOptions.repeat) {
        url += '&repeat=true';
    }
    
    // Set audio source and play
    audioElement.src = url;
    audioElement.playbackRate = playbackOptions.speed;
    speedControl.value = playbackOptions.speed;
    speedValue.textContent = `${playbackOptions.speed.toFixed(1)}x`;
    
    // Update audio info
    fetchAudioInfo(audioId);
    
    // Play audio
    audioElement.play();
}

/**
 * Fetch audio file metadata
 * @param {string} audioId - ID of the audio file
 */
async function fetchAudioInfo(audioId) {
    try {
        const response = await fetch(`/api/audio/${audioId}`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch audio info: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update UI with audio info
        audioTitle.textContent = data.name || `Audio ${audioId}`;
        
        // Build description from metadata
        let description = '';
        
        if (data.content_type) {
            description += `Type: ${data.content_type} | `;
        }
        
        if (data.languages) {
            description += `Languages: ${data.languages.join(', ')} | `;
        }
        
        if (data.duration) {
            const minutes = Math.floor(data.duration / 60);
            const seconds = Math.floor(data.duration % 60);
            description += `Duration: ${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
        
        audioDescription.textContent = description;
    } catch (error) {
        console.error('Error fetching audio info:', error);
        audioTitle.textContent = `Audio ${audioId}`;
        audioDescription.textContent = 'No additional information available';
    }
}

/**
 * Load audio library from API
 */
async function loadAudioLibrary() {
    // This would normally fetch from the API
    // For now, we'll use placeholder data
    const audioFiles = [
        {
            id: 'sample1',
            name: 'Sing Along! - London Bridge',
            content_type: 'song',
            languages: ['en', 'ja', 'fr'],
            duration: 225
        },
        {
            id: 'sample2',
            name: 'Multilingual Friends - Episode 1',
            content_type: 'story',
            languages: ['en', 'es', 'de'],
            duration: 150
        },
        {
            id: 'sample3',
            name: 'Hippo Goes Overseas - Chapter 1',
            content_type: 'story',
            languages: ['en', 'ja', 'fr', 'es'],
            duration: 320
        },
        {
            id: 'sample4',
            name: 'KABAJIN - Who Am I?',
            content_type: 'story',
            languages: ['ja', 'en', 'zh', 'ko'],
            duration: 180
        }
    ];
    
    renderAudioLibrary(audioFiles);
}

/**
 * Render audio library items
 * @param {Array} audioFiles - Array of audio file objects
 */
function renderAudioLibrary(audioFiles) {
    // Clear existing items
    audioList.innerHTML = '';
    
    // Filter audio files based on search and filters
    const searchTerm = searchInput.value.toLowerCase();
    const languageFilterValue = languageFilter.value;
    const contentFilterValue = contentFilter.value;
    
    const filteredFiles = audioFiles.filter(file => {
        // Search filter
        const matchesSearch = file.name.toLowerCase().includes(searchTerm);
        
        // Language filter
        const matchesLanguage = languageFilterValue === 'all' || 
            (file.languages && file.languages.includes(languageFilterValue));
        
        // Content type filter
        const matchesContent = contentFilterValue === 'all' || 
            file.content_type === contentFilterValue;
        
        return matchesSearch && matchesLanguage && matchesContent;
    });
    
    // Render filtered files
    filteredFiles.forEach(file => {
        const minutes = Math.floor(file.duration / 60);
        const seconds = Math.floor(file.duration % 60);
        const durationStr = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        const audioItem = document.createElement('div');
        audioItem.className = 'audio-item';
        audioItem.innerHTML = `
            <div class="audio-item-info">
                <h3>${file.name}</h3>
                <p>Languages: ${file.languages ? file.languages.join(', ').toUpperCase() : 'Unknown'}</p>
                <p>Duration: ${durationStr}</p>
            </div>
            <button class="play-button" data-id="${file.id}">Play</button>
        `;
        
        // Add event listener to play button
        const playButton = audioItem.querySelector('.play-button');
        playButton.addEventListener('click', function() {
            playAudio(file.id);
        });
        
        audioList.appendChild(audioItem);
    });
}

// Search and filter functionality
searchInput.addEventListener('input', function() {
    loadAudioLibrary();
});

languageFilter.addEventListener('change', function() {
    loadAudioLibrary();
});

contentFilter.addEventListener('change', function() {
    loadAudioLibrary();
});

// Agent interaction functionality
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

/**
 * Send message to agent
 */
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Clear input
    userInput.value = '';
    
    try {
        // Send message to agent
        const response = await fetch('/api/agent/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to send message: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add agent response to chat
        addMessageToChat(data.message || 'I apologize, but I am still learning to respond to that type of request.', 'agent');
    } catch (error) {
        console.error('Error sending message:', error);
        addMessageToChat('Sorry, there was an error processing your request. Please try again later.', 'agent');
    }
}

/**
 * Add message to chat history
 * @param {string} message - Message text
 * @param {string} sender - Message sender ('user' or 'agent')
 */
function addMessageToChat(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}-message`;
    messageElement.innerHTML = `<p>${message}</p>`;
    
    chatHistory.appendChild(messageElement);
    
    // Scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Load audio library
    loadAudioLibrary();
});
