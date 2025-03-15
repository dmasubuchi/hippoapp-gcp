"""
Configuration for the Agentspace app module.
"""

# Application configuration
APP_CONFIG = {
    "name": "HippoLingua",
    "version": "0.1.0",
    "description": "Hippo Family Club multilingual learning application",
    "host": "0.0.0.0",
    "port": 8080,
}

# Google Cloud Storage configuration
GCS_CONFIG = {
    "bucket_name": "hippoapp-audio-storage",
    "project_id": "hippoapp-gcp",
}

# Audio playback configuration
PLAYBACK_CONFIG = {
    "supported_formats": ["mp3", "wav", "flac", "ogg"],
    "default_speed": 1.0,
    "speed_range": [0.5, 2.0],
    "buffer_size": 4096,
    "enable_caching": True,
    "cache_directory": "/tmp/hippoapp-cache",
}

# Agentspace configuration
AGENTSPACE_CONFIG = {
    "api_key": "YOUR_AGENTSPACE_API_KEY",
    "api_url": "https://api.agentspace.ai/v1",
    "agents": {
        "learning_agent": {
            "config_path": "agents/learning_agent/config.json",
            "capabilities": [
                "learning_support",
                "pronunciation_practice",
                "role_playing",
                "progress_tracking",
                "personalization",
            ],
        },
    },
}

# User data configuration
USER_DATA_CONFIG = {
    "storage_type": "firestore",
    "collection_name": "user_data",
    "fields": [
        "user_id",
        "name",
        "email",
        "learning_history",
        "preferences",
        "progress",
        "achievements",
    ],
}
