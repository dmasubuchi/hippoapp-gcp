"""
Configuration for the data ingestion module.
"""

# Google Cloud Storage configuration
GCS_CONFIG = {
    "bucket_name": "hippoapp-audio-storage",
    "project_id": "hippoapp-gcp",
}

# Google Cloud Speech-to-Text configuration
SPEECH_TO_TEXT_CONFIG = {
    "audio_encoding": "LINEAR16",
    "sample_rate_hertz": 16000,
    "language_codes": [
        "en-US",  # English
        "ja-JP",  # Japanese
        "fr-FR",  # French
        "es-ES",  # Spanish
        "de-DE",  # German
        "it-IT",  # Italian
        "zh-CN",  # Chinese (Simplified)
        "ko-KR",  # Korean
        "ru-RU",  # Russian
        "pt-BR",  # Portuguese
        "ar-SA",  # Arabic
    ],
    "enable_speaker_diarization": True,
    "diarization_speaker_count": 3,
}

# Google Cloud Translation API configuration
TRANSLATION_CONFIG = {
    "project_id": "hippoapp-gcp",
}

# Audio processing configuration
AUDIO_PROCESSING_CONFIG = {
    "supported_formats": ["mp3", "wav", "flac", "ogg"],
    "max_file_size_mb": 100,
    "temp_directory": "/tmp/hippoapp-audio",
}

# Metadata schema
METADATA_SCHEMA = {
    "required_fields": [
        "title",
        "languages",
        "duration",
        "content_type",  # song, story, etc.
    ],
    "optional_fields": [
        "description",
        "characters",
        "tags",
        "difficulty_level",
        "age_range",
    ],
}
