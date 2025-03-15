"""
Configuration settings for the application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Debug mode
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Secret key
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

# GCP configuration
GCS_CONFIG = {
    "bucket_name": "language-learning-audio",
    "project_id": "lucid-inquiry-453823-b0",
    "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
}

# Audio playback configuration
PLAYBACK_CONFIG = {
    "supported_formats": ["mp3", "wav", "flac", "ogg"],
    "default_speed": 1.0,
    "speed_range": [0.5, 2.0],
    "buffer_size": 4096,
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": os.path.join(BASE_DIR, "logs", "app.log"),
}

# API configuration
API_CONFIG = {
    "version": "v1",
    "prefix": "/api",
}
