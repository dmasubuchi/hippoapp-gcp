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
const prevLanguageBtn = document.getElementById('prev-language');
const nextLanguageBtn = document.getElementById('next-language');
const currentLanguageEl = document.getElementById('current-language');
const sentenceContainer = document.getElementById('sentence-container');

// Audio player functionality
speedControl.addEventListener('input', function() {
    const speed = parseFloat(this.value);
    audioElement.playbackRate = speed;
    speedValue.textContent = `${speed.toFixed(1)}x`;
});

// Language and sentence tracking
const LANGUAGES = [
    { code: 'en', name: 'English' },
    { code: 'ja', name: 'Japanese' },
    { code: 'fr', name: 'French' },
    { code: 'es', name: 'Spanish' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ko', name: 'Korean' },
    { code: 'ru', name: 'Russian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'ar', name: 'Arabic' }
];

let currentLanguageIndex = 0;
let currentSentenceIndex = 0;
let sentences = {}; // Will store sentences for each language
let currentAudioId = null;

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
    
    // Store current audio ID
    currentAudioId = audioId;
    
    // Load sentences for all languages
    currentLanguageIndex = 0; // Reset to first language
    currentLanguageEl.textContent = LANGUAGES[currentLanguageIndex].name;
    
    // Load sentences for current language
    loadSentences(audioId, LANGUAGES[currentLanguageIndex].code);
    
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

/**
 * Load sentences for a specific language
 * @param {string} audioId - ID of the audio file
 * @param {string} languageCode - Language code
 */
async function loadSentences(audioId, languageCode) {
    try {
        // This would normally fetch from the API
        // For now, we'll use placeholder data
        const mockSentences = generateMockSentences(audioId, languageCode);
        sentences[languageCode] = mockSentences;
        
        if (languageCode === LANGUAGES[currentLanguageIndex].code) {
            renderSentences(mockSentences);
        }
        
        return mockSentences;
    } catch (error) {
        console.error('Error loading sentences:', error);
        return [];
    }
}

/**
 * Generate mock sentences for demo purposes
 * This would be replaced with actual API data in production
 */
function generateMockSentences(audioId, languageCode) {
    const sentenceCount = 10;
    const mockSentences = [];
    const baseTime = 10; // seconds per sentence
    
    // Different text for different languages
    const textByLanguage = {
        'en': [
            "Hello, how are you?",
            "I'm learning multiple languages.",
            "The weather is nice today.",
            "I like to travel around the world.",
            "Music helps me learn languages.",
            "Let's practice speaking together.",
            "What time is it now?",
            "I'm hungry, let's eat something.",
            "This is a great learning app.",
            "See you tomorrow!"
        ],
        'ja': [
            "こんにちは、お元気ですか？",
            "私は複数の言語を学んでいます。",
            "今日は天気がいいですね。",
            "世界中を旅行するのが好きです。",
            "音楽は言語学習に役立ちます。",
            "一緒に会話の練習をしましょう。",
            "今何時ですか？",
            "お腹が空きました、何か食べましょう。",
            "これは素晴らしい学習アプリです。",
            "また明日会いましょう！"
        ],
        'fr': [
            "Bonjour, comment allez-vous ?",
            "J'apprends plusieurs langues.",
            "Il fait beau aujourd'hui.",
            "J'aime voyager autour du monde.",
            "La musique m'aide à apprendre les langues.",
            "Pratiquons ensemble.",
            "Quelle heure est-il maintenant ?",
            "J'ai faim, mangeons quelque chose.",
            "C'est une excellente application d'apprentissage.",
            "À demain !"
        ]
    };
    
    // Default to English if language not found
    const texts = textByLanguage[languageCode] || textByLanguage['en'];
    
    for (let i = 0; i < sentenceCount; i++) {
        const startTime = i * baseTime;
        const endTime = startTime + baseTime;
        
        mockSentences.push({
            id: `${audioId}-${languageCode}-${i}`,
            text: texts[i % texts.length],
            startTime: startTime,
            endTime: endTime,
            languageCode: languageCode
        });
    }
    
    return mockSentences;
}

/**
 * Render sentences in the UI
 * @param {Array} sentenceList - List of sentences to render
 */
function renderSentences(sentenceList) {
    sentenceContainer.innerHTML = '';
    
    sentenceList.forEach((sentence, index) => {
        const sentenceEl = document.createElement('div');
        sentenceEl.className = 'sentence';
        sentenceEl.dataset.index = index;
        
        const minutes = Math.floor(sentence.startTime / 60);
        const seconds = Math.floor(sentence.startTime % 60);
        const timeStr = `[${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}]`;
        
        sentenceEl.innerHTML = `
            <span class="sentence-time">${timeStr}</span>
            <span class="sentence-text">${sentence.text}</span>
        `;
        
        sentenceEl.addEventListener('click', () => {
            jumpToSentence(index);
        });
        
        sentenceContainer.appendChild(sentenceEl);
    });
}

/**
 * Jump to a specific sentence
 * @param {number} index - Index of the sentence to jump to
 */
function jumpToSentence(index) {
    const currentLanguage = LANGUAGES[currentLanguageIndex].code;
    const sentenceList = sentences[currentLanguage];
    
    if (!sentenceList || index >= sentenceList.length) {
        return;
    }
    
    currentSentenceIndex = index;
    const sentence = sentenceList[index];
    
    // Update audio playback position
    audioElement.currentTime = sentence.startTime;
    
    // Highlight the current sentence
    highlightCurrentSentence();
    
    // Start playback if paused
    if (audioElement.paused) {
        audioElement.play();
    }
}

/**
 * Highlight the current sentence
 */
function highlightCurrentSentence() {
    // Remove active class from all sentences
    document.querySelectorAll('.sentence').forEach(el => {
        el.classList.remove('active');
    });
    
    // Add active class to current sentence
    const sentenceEl = document.querySelector(`.sentence[data-index="${currentSentenceIndex}"]`);
    if (sentenceEl) {
        sentenceEl.classList.add('active');
        
        // Scroll to the sentence if not visible
        const containerRect = sentenceContainer.getBoundingClientRect();
        const sentenceRect = sentenceEl.getBoundingClientRect();
        
        if (sentenceRect.top < containerRect.top || sentenceRect.bottom > containerRect.bottom) {
            sentenceEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

/**
 * Switch to a different language
 * @param {number} direction - Direction to switch (-1 for previous, 1 for next)
 */
function switchLanguage(direction) {
    const newIndex = (currentLanguageIndex + direction + LANGUAGES.length) % LANGUAGES.length;
    const newLanguage = LANGUAGES[newIndex];
    const oldLanguage = LANGUAGES[currentLanguageIndex];
    
    // Update current language index
    currentLanguageIndex = newIndex;
    
    // Update UI
    currentLanguageEl.textContent = newLanguage.name;
    
    // Load sentences for the new language if not already loaded
    if (!sentences[newLanguage.code]) {
        loadSentences(currentAudioId, newLanguage.code).then(() => {
            // Find corresponding sentence in new language
            syncSentencePosition(oldLanguage.code, newLanguage.code);
        });
    } else {
        // Find corresponding sentence in new language
        syncSentencePosition(oldLanguage.code, newLanguage.code);
    }
}

/**
 * Synchronize sentence position when switching languages
 * @param {string} fromLang - Source language code
 * @param {string} toLang - Target language code
 */
function syncSentencePosition(fromLang, toLang) {
    const fromSentences = sentences[fromLang];
    const toSentences = sentences[toLang];
    
    if (!fromSentences || !toSentences) {
        return;
    }
    
    // Find the current sentence in the source language
    const currentSentence = fromSentences[currentSentenceIndex];
    
    // Find the corresponding sentence in the target language
    // For now, we'll use the same index, but in a real implementation
    // this would match based on meaning or time position
    renderSentences(toSentences);
    highlightCurrentSentence();
    
    // Update audio playback position
    if (toSentences[currentSentenceIndex]) {
        audioElement.currentTime = toSentences[currentSentenceIndex].startTime;
    }
}

// Language navigation event listeners
prevLanguageBtn.addEventListener('click', () => {
    switchLanguage(-1);
});

nextLanguageBtn.addEventListener('click', () => {
    switchLanguage(1);
});

// Add swipe gesture support for mobile
let touchStartX = 0;
let touchEndX = 0;

sentenceContainer.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

sentenceContainer.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    if (touchEndX < touchStartX - swipeThreshold) {
        // Swipe left - next language
        switchLanguage(1);
    } else if (touchEndX > touchStartX + swipeThreshold) {
        // Swipe right - previous language
        switchLanguage(-1);
    }
}

// Audio timeupdate event to track current sentence
audioElement.addEventListener('timeupdate', () => {
    const currentTime = audioElement.currentTime;
    const currentLanguage = LANGUAGES[currentLanguageIndex].code;
    const sentenceList = sentences[currentLanguage];
    
    if (!sentenceList) {
        return;
    }
    
    // Find the current sentence based on time
    for (let i = 0; i < sentenceList.length; i++) {
        const sentence = sentenceList[i];
        if (currentTime >= sentence.startTime && currentTime < sentence.endTime) {
            if (currentSentenceIndex !== i) {
                currentSentenceIndex = i;
                highlightCurrentSentence();
            }
            break;
        }
    }
});

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Load audio library
    loadAudioLibrary();
});
