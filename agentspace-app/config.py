"""
Configuration settings for the application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Application configuration
APP_CONFIG = {
    "title": "Hippo Family Club - Multilingual Audio Player",
    "description": "A multilingual audio player for language learning",
    "version": "1.0.0",
    "debug": os.getenv("DEBUG", "False").lower() in ("true", "1", "t"),
}

# Google Cloud Storage configuration
GCS_CONFIG = {
    "project_id": os.getenv("GCP_PROJECT_ID", "lucid-inquiry-453823-b0"),
    "bucket_name": os.getenv("GCP_STORAGE_BUCKET", "language-learning-audio"),
    "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
}

# Audio configuration
AUDIO_CONFIG = {
    "formats": ["mp3", "wav", "ogg"],
    "max_duration": 3600,  # Maximum duration in seconds
    "default_speed": 1.0,
}

# Language configuration
LANGUAGE_CONFIG = {
    "default": "en",
    "supported": {
        "en": {
            "name": "English",
            "display_name": "English",
            "flag": "🇺🇸",
        },
        "ja": {
            "name": "Japanese",
            "display_name": "日本語",
            "flag": "🇯🇵",
        },
        "fr": {
            "name": "French",
            "display_name": "Français",
            "flag": "🇫🇷",
        },
        "es": {
            "name": "Spanish",
            "display_name": "Español",
            "flag": "🇪🇸",
        },
        "de": {
            "name": "German",
            "display_name": "Deutsch",
            "flag": "🇩🇪",
        },
    },
}
