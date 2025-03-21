"""
Utility functions for the Hippo Family Club language learning app.
"""
import os
import logging
import tempfile
from pathlib import Path
import sys
from google.cloud import storage
from google.oauth2 import service_account
from pydub import AudioSegment
from fastapi.responses import StreamingResponse
import io

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import GCS_CONFIG, AUDIO_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global clients
storage_client = None

def setup_gcp_services():
    """Initialize GCP services with credentials."""
    global storage_client
    
    try:
        # Get credentials path from environment
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        
        # Check if we're in debug mode
        debug_mode = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")
        
        if debug_mode:
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
            try:
                credentials = service_account.Credentials.from_service_account_file(credentials_path)
                storage_client = storage.Client(
                    project=GCS_CONFIG["project_id"],
                    credentials=credentials
                )
            except Exception as e:
                logger.error(f"Error loading credentials from {credentials_path}: {str(e)}")
                if debug_mode:
                    logger.warning("Continuing with mock services for local development")
                    storage_client = None
                    return
                raise
        else:
            logger.warning(f"Credentials path not found or invalid: {credentials_path}")
            if not credentials_path:
                logger.warning("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
            elif not os.path.exists(credentials_path):
                logger.warning(f"Credentials file does not exist at: {credentials_path}")
            elif os.path.getsize(credentials_path) == 0:
                logger.warning(f"Credentials file exists but is empty: {credentials_path}")
                
            if debug_mode:
                logger.warning("Debug mode enabled, continuing without GCP services")
                storage_client = None
                return
                
            logger.info("Attempting to use application default credentials")
            try:
                storage_client = storage.Client(project=GCS_CONFIG["project_id"])
            except Exception as e:
                logger.error(f"Failed to initialize with application default credentials: {str(e)}")
                raise
            
        logger.info("GCP services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing GCP services: {str(e)}")
        if debug_mode:
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
        setup_gcp_services()
        
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
        raise

def get_language_from_path(path):
    """
    Extract language code from file path.
    
    Args:
        path: File path (e.g., 'audio/en/lesson1.mp3')
        
    Returns:
        str: Language code (e.g., 'en') or 'unknown' if not found
    """
    # Common language codes in paths
    language_patterns = {
        '/en/': 'en',    # English
        '/ja/': 'ja',    # Japanese
        '/fr/': 'fr',    # French
        '/es/': 'es',    # Spanish
        '/de/': 'de',    # German
        '/zh/': 'zh',    # Chinese
        '/ko/': 'ko',    # Korean
        '/it/': 'it',    # Italian
        '/ru/': 'ru',    # Russian
        '/pt/': 'pt'     # Portuguese
    }
    
    # Check for language code in path
    for pattern, lang_code in language_patterns.items():
        if pattern in path:
            return lang_code
            
    # Alternative method: extract from path segments
    parts = path.split('/')
    for part in parts:
        if len(part) == 2 and part.isalpha():
            return part
            
    return 'unknown'

def get_audio_file(file_id):
    """
    Get audio file metadata from Google Cloud Storage.
    
    Args:
        file_id: ID of the audio file
        
    Returns:
        dict: Audio file metadata
    """
    global storage_client
    
    if storage_client is None:
        setup_gcp_services()
        
    # For local development with mock data
    debug_mode = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")
    if debug_mode and storage_client is None:
        logger.warning(f"Using mock audio data for {file_id}")
        language = "en"
        if "/ja/" in file_id:
            language = "ja"
        elif "/fr/" in file_id:
            language = "fr"
            
        return {
            "id": file_id,
            "name": os.path.basename(file_id),
            "size": 1024,
            "updated": "2025-03-15T00:00:00Z",
            "content_type": "audio/mpeg",
            "language": language
        }
    
    try:
        # Get bucket
        bucket = storage_client.bucket(GCS_CONFIG["bucket_name"])
        
        # List blobs with prefix
        blobs = list(bucket.list_blobs(prefix=f"audio/{file_id}"))
        
        if not blobs:
            raise ValueError(f"Audio file {file_id} not found")
        
        # Get the first matching blob
        blob = blobs[0]
        
        # Get metadata
        metadata = {
            "id": file_id,
            "name": blob.name,
            "size": blob.size,
            "content_type": blob.content_type,
            "updated": blob.updated.isoformat(),
            "url": f"gs://{GCS_CONFIG['bucket_name']}/{blob.name}",
            "language": get_language_from_path(blob.name)
        }
        
        return metadata
    except Exception as e:
        logger.error(f"Error getting audio file {file_id}: {str(e)}")
        if debug_mode:
            logger.warning("Returning mock data for local development")
            return {
                "id": file_id,
                "name": os.path.basename(file_id),
                "size": 1024,
                "content_type": "audio/mpeg",
                "language": "en"
            }
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
    # This is a placeholder function that would use the transcription API
    # to extract sentences with time tags from the "language-learning-audio" bucket
    # For now, we'll return an empty list
    return []

def process_audio_playback(file_id, start_time=0, end_time=None, speed=1.0, repeat=False):
    """
    Process audio file for playback with streaming response.
    
    Args:
        file_id: File ID (path in bucket)
        start_time: Start time in seconds
        end_time: End time in seconds
        speed: Playback speed (0.5 to 2.0)
        repeat: Whether to repeat the audio
        
    Returns:
        StreamingResponse: Audio data stream
    """
    # Check if we're in debug mode
    debug_mode = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")
    
    try:
        # For debug mode with no storage client, return mock audio
        if debug_mode and (storage_client is None):
            logger.info(f"Debug mode: Generating mock audio for {file_id}")
            
            # Create a simple audio segment for testing
            # Different sounds for different languages
            if "/ja/" in file_id:
                # Japanese - higher pitch tone
                audio = AudioSegment.silent(duration=500)
                for i in range(10):
                    tone = AudioSegment.sine(440 + (i * 50), duration=500)
                    audio += tone
            elif "/fr/" in file_id:
                # French - lower pitch tone
                audio = AudioSegment.silent(duration=500)
                for i in range(10):
                    tone = AudioSegment.sine(330 + (i * 40), duration=500)
                    audio += tone
            else:
                # Default/English - medium pitch tone
                audio = AudioSegment.silent(duration=500)
                for i in range(10):
                    tone = AudioSegment.sine(380 + (i * 45), duration=500)
                    audio += tone
            
            # Apply speed change if needed
            if speed != 1.0:
                # Ensure speed is within reasonable bounds
                speed = max(0.5, min(2.0, speed))
                audio = audio.speedup(playback_speed=speed)
            
            # Apply repeat if needed
            if repeat:
                audio = audio * 3
            
            # Export to buffer
            buffer = io.BytesIO()
            audio.export(buffer, format="mp3")
            buffer.seek(0)
            
            # Return streaming response
            return StreamingResponse(
                buffer, 
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename=mock-{os.path.basename(file_id)}"}
            )
        
        # For production: Get audio file from GCS
        # First get metadata
        metadata = get_audio_file(file_id)
        
        # Then download the actual audio file
        bucket = storage_client.bucket(GCS_CONFIG["bucket_name"])
        blob = bucket.blob(metadata["name"])
        
        # Download to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        blob.download_to_filename(temp_file.name)
        temp_file.close()
        
        try:
            # Load audio with pydub
            audio = AudioSegment.from_file(temp_file.name)
            
            # Apply start and end times
            start_ms = int(start_time * 1000)
            end_ms = int(end_time * 1000) if end_time is not None else len(audio)
            
            # Ensure start and end times are within bounds
            start_ms = max(0, min(start_ms, len(audio)))
            end_ms = max(start_ms, min(end_ms, len(audio)))
            
            # Extract segment
            segment = audio[start_ms:end_ms]
            
            # Apply speed change
            if speed != 1.0:
                # Ensure speed is within reasonable bounds
                speed = max(0.5, min(2.0, speed))
                segment = segment.speedup(playback_speed=speed)
            
            # Apply repeat if needed
            if repeat:
                segment = segment * 3  # Repeat 3 times
            
            # Convert to bytes
            output = io.BytesIO()
            segment.export(output, format="mp3")
            output.seek(0)
            
            # Return streaming response
            return StreamingResponse(
                output, 
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename={os.path.basename(file_id)}"}
            )
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
                
    except Exception as e:
        logger.error(f"Error processing audio file {file_id}: {str(e)}")
        if debug_mode:
            logger.warning("Generating mock audio for error case")
            audio = AudioSegment.silent(duration=3000)  # 3 seconds of silence
            buffer = io.BytesIO()
            audio.export(buffer, format="mp3")
            buffer.seek(0)
            return StreamingResponse(
                buffer, 
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename=error-audio.mp3"}
            )
        raise
