"""
Utility functions for the application.
"""
import os
import logging
from google.cloud import storage
from google.oauth2 import service_account
from pydub import AudioSegment
from fastapi.responses import StreamingResponse
from io import BytesIO

from config import GCS_CONFIG, APP_CONFIG

# Configure logging
logger = logging.getLogger(__name__)

# Global variables
storage_client = None

def init_gcp_services():
    """
    Initialize GCP services with credentials.
    """
    global storage_client
    
    try:
        credentials_path = GCS_CONFIG.get("credentials_path")
        
        # For local development with mock credentials
        if APP_CONFIG.get("debug", False):
            logger.warning("Debug mode enabled, using mock credentials for local development")
            try:
                # Try to use default credentials
                storage_client = storage.Client(project=GCS_CONFIG["project_id"])
                logger.info("Successfully initialized with default credentials")
            except Exception as e:
                logger.warning(f"Could not initialize with default credentials: {str(e)}")
                # Continue without a storage client for local development
                storage_client = None
            return
            
        # For production with real credentials
        if credentials_path and os.path.exists(credentials_path):
            logger.info(f"Using service account credentials from: {credentials_path}")
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            storage_client = storage.Client(
                project=GCS_CONFIG["project_id"],
                credentials=credentials
            )
        else:
            logger.info("Using application default credentials")
            storage_client = storage.Client(project=GCS_CONFIG["project_id"])
            
        logger.info("GCP services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing GCP services: {str(e)}")
        if APP_CONFIG.get("debug", False):
            logger.warning("Continuing with mock services for local development")
            storage_client = None
        else:
            raise

def list_audio_files(prefix=None, limit=100):
    """
    List audio files in the GCS bucket.
    
    Args:
        prefix: Optional prefix to filter files
        limit: Maximum number of files to return
        
    Returns:
        List of file metadata
    """
    if storage_client is None:
        init_gcp_services()
        
    # For local development with mock data
    if APP_CONFIG.get("debug", False) and storage_client is None:
        logger.warning("Using mock audio file list for local development")
        return [
            {
                "id": "audio/en/lesson1.mp3",
                "name": "lesson1.mp3",
                "size": 1024,
                "updated": "2025-03-15T00:00:00Z",
                "content_type": "audio/mpeg",
                "language": "en"
            },
            {
                "id": "audio/ja/lesson1.mp3",
                "name": "lesson1.mp3",
                "size": 2048,
                "updated": "2025-03-15T00:00:00Z",
                "content_type": "audio/mpeg",
                "language": "ja"
            },
            {
                "id": "audio/fr/lesson1.mp3",
                "name": "lesson1.mp3",
                "size": 2048,
                "updated": "2025-03-15T00:00:00Z",
                "content_type": "audio/mpeg",
                "language": "fr"
            }
        ]
        
    try:
        bucket = storage_client.get_bucket(GCS_CONFIG["bucket_name"])
        blobs = bucket.list_blobs(prefix=prefix, max_results=limit)
        
        files = []
        for blob in blobs:
            # Only include audio files
            if blob.name.endswith(('.mp3', '.wav', '.ogg')):
                files.append({
                    "id": blob.name,
                    "name": os.path.basename(blob.name),
                    "size": blob.size,
                    "updated": blob.updated,
                    "content_type": blob.content_type,
                    "language": get_language_from_path(blob.name)
                })
        
        return files
    except Exception as e:
        logger.error(f"Error listing audio files: {str(e)}")
        if APP_CONFIG.get("debug", False):
            logger.warning("Returning mock data for local development")
            return [
                {
                    "id": "audio/en/lesson1.mp3",
                    "name": "lesson1.mp3",
                    "size": 1024,
                    "updated": "2025-03-15T00:00:00Z",
                    "content_type": "audio/mpeg",
                    "language": "en"
                }
            ]
        raise

def get_language_from_path(path):
    """
    Extract language code from file path.
    
    Args:
        path: File path
        
    Returns:
        Language code or None
    """
    # Example path: audio/en/lesson1.mp3
    parts = path.split('/')
    if len(parts) >= 2:
        lang_code = parts[1]
        if len(lang_code) == 2:  # Simple validation for language code
            return lang_code
    return None

def get_audio_file(file_id):
    """
    Get audio file from GCS bucket.
    
    Args:
        file_id: File ID (path in bucket)
        
    Returns:
        Audio file data
    """
    if storage_client is None:
        init_gcp_services()
        
    # For local development with mock data
    if APP_CONFIG.get("debug", False) and storage_client is None:
        logger.warning(f"Using mock audio data for {file_id}")
        # Create a simple audio segment for testing
        audio = AudioSegment.silent(duration=5000)  # 5 seconds of silence
        buffer = BytesIO()
        audio.export(buffer, format="mp3")
        buffer.seek(0)
        return buffer
        
    try:
        bucket = storage_client.get_bucket(GCS_CONFIG["bucket_name"])
        blob = bucket.blob(file_id)
        
        # Download to memory
        data = BytesIO()
        blob.download_to_file(data)
        data.seek(0)
        
        return data
    except Exception as e:
        logger.error(f"Error downloading audio file {file_id}: {str(e)}")
        if APP_CONFIG.get("debug", False):
            logger.warning("Returning mock audio data for local development")
            audio = AudioSegment.silent(duration=5000)  # 5 seconds of silence
            buffer = BytesIO()
            audio.export(buffer, format="mp3")
            buffer.seek(0)
            return buffer
        raise

def extract_sentences(audio_file_path, language_code):
    """
    Extract sentences from audio file with time tags.
    
    Args:
        audio_file_path: Path to the audio file
        language_code: Language code for transcription
        
    Returns:
        List of sentences with time tags
    """
    # For local development with mock data
    if APP_CONFIG.get("debug", False):
        logger.warning(f"Using mock sentence data for {language_code}")
        if language_code == "en":
            return [
                {"start_time": 0, "end_time": 5, "text": "Hello, how are you?"},
                {"start_time": 6, "end_time": 10, "text": "I'm doing well, thank you."},
                {"start_time": 11, "end_time": 15, "text": "What a beautiful day!"}
            ]
        elif language_code == "ja":
            return [
                {"start_time": 0, "end_time": 5, "text": "こんにちは、お元気ですか？"},
                {"start_time": 6, "end_time": 10, "text": "はい、元気です。ありがとう。"},
                {"start_time": 11, "end_time": 15, "text": "いい天気ですね！"}
            ]
        elif language_code == "fr":
            return [
                {"start_time": 0, "end_time": 5, "text": "Bonjour, comment allez-vous?"},
                {"start_time": 6, "end_time": 10, "text": "Je vais bien, merci."},
                {"start_time": 11, "end_time": 15, "text": "Quelle belle journée!"}
            ]
        else:
            return []
    
    # This would use the transcription API in production
    # to extract sentences with time tags from the "language-learning-audio" bucket
    return []

def process_audio_playback(file_id, start_time=0, end_time=None, speed=1.0, repeat=False):
    """
    Process audio file for playback.
    
    Args:
        file_id: File ID (path in bucket)
        start_time: Start time in seconds
        end_time: End time in seconds
        speed: Playback speed
        repeat: Whether to repeat the audio
        
    Returns:
        Streaming response with audio data
    """
    try:
        # Get audio file
        audio_data = get_audio_file(file_id)
        
        # Load audio with pydub
        audio = AudioSegment.from_file(audio_data)
        
        # Apply start and end times
        start_ms = start_time * 1000
        end_ms = end_time * 1000 if end_time is not None else len(audio)
        
        # Ensure start and end times are within bounds
        start_ms = max(0, min(start_ms, len(audio)))
        end_ms = max(start_ms, min(end_ms, len(audio)))
        
        # Extract segment
        segment = audio[start_ms:end_ms]
        
        # Apply speed change
        if speed != 1.0:
            segment = segment.speedup(playback_speed=speed)
        
        # Apply repeat if needed
        if repeat:
            segment = segment * 3  # Repeat 3 times
        
        # Convert to bytes
        output = BytesIO()
        segment.export(output, format="mp3")
        output.seek(0)
        
        # Return streaming response
        return StreamingResponse(
            output, 
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename={os.path.basename(file_id)}"}
        )
    except Exception as e:
        logger.error(f"Error processing audio file {file_id}: {str(e)}")
        if APP_CONFIG.get("debug", False):
            logger.warning("Returning mock audio data for local development")
            audio = AudioSegment.silent(duration=5000)  # 5 seconds of silence
            buffer = BytesIO()
            audio.export(buffer, format="mp3")
            buffer.seek(0)
            return StreamingResponse(
                buffer, 
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename=mock-audio.mp3"}
            )
        raise
