"""
Configuration for the Hippo Family Club language learning app.
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
    "host": os.environ.get("HOST", "0.0.0.0"),
    "port": int(os.environ.get("PORT", 8080)),
    "debug": os.environ.get("DEBUG", "False").lower() in ("true", "1", "t"),
}

# Google Cloud Storage configuration
GCS_CONFIG = {
    "project_id": os.environ.get("GCP_PROJECT_ID", "lucid-inquiry-453823-b0"),
    "bucket_name": os.environ.get("GCP_STORAGE_BUCKET", "language-learning-audio"),
    "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
}

# Audio configuration
AUDIO_CONFIG = {
    "formats": ["mp3", "wav", "ogg"],
    "cache_directory": os.environ.get("AUDIO_CACHE_DIR", "/tmp/hippoapp-cache"),
    "max_duration": 3600,  # Maximum audio duration in seconds
    "default_speed": 1.0,
    "speed_range": {
        "min": 0.5,
        "max": 2.0,
        "step": 0.1
    }
}

# Language configuration
LANGUAGE_CONFIG = {
    "default": "en",
    "supported": {
        "en": {
            "name": "English",
            "display_name": "English",
            "flag": "🇺🇸",
            "direction": "ltr"
        },
        "ja": {
            "name": "Japanese",
            "display_name": "日本語",
            "flag": "🇯🇵",
            "direction": "ltr"
        },
        "fr": {
            "name": "French",
            "display_name": "Français",
            "flag": "🇫🇷",
            "direction": "ltr"
        },
        "es": {
            "name": "Spanish",
            "display_name": "Español",
            "flag": "🇪🇸",
            "direction": "ltr"
        },
        "de": {
            "name": "German",
            "display_name": "Deutsch",
            "flag": "🇩🇪",
            "direction": "ltr"
        },
        "zh": {
            "name": "Chinese",
            "display_name": "中文",
            "flag": "🇨🇳",
            "direction": "ltr"
        },
        "ko": {
            "name": "Korean",
            "display_name": "한국어",
            "flag": "🇰🇷",
            "direction": "ltr"
        }
    }
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
