"""
Utility functions for the application.
"""
import os
import logging
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

from google.cloud import storage
from google.oauth2 import service_account
from pydub import AudioSegment

from config import GCS_CONFIG, LOGGING_CONFIG

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
formatter = logging.Formatter(LOGGING_CONFIG["format"])

# Create log directory if it doesn't exist
log_dir = Path(LOGGING_CONFIG["file"]).parent
log_dir.mkdir(exist_ok=True)

# Add file handler
file_handler = logging.FileHandler(LOGGING_CONFIG["file"])
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Initialize GCP clients
storage_client = None

def init_gcp_services():
    """
    Initialize GCP services with credentials.
    """
    global storage_client
    
    try:
        # Check if credentials path is provided
        credentials_path = GCS_CONFIG.get("credentials_path")
        
        if credentials_path and os.path.exists(credentials_path):
            # Use explicit credentials
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            storage_client = storage.Client(
                project=GCS_CONFIG["project_id"],
                credentials=credentials
            )
        else:
            # Use application default credentials
            storage_client = storage.Client(project=GCS_CONFIG["project_id"])
            
        logger.info("GCP services initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing GCP services: {str(e)}")
        raise

# Initialize GCP services on module import
try:
    init_gcp_services()
except Exception as e:
    logger.error(f"Failed to initialize GCP services: {str(e)}")

def list_audio_files(prefix: str = None) -> List[Dict[str, Any]]:
    """
    List audio files in the GCS bucket.
    
    Args:
        prefix: Optional prefix to filter files
        
    Returns:
        List of audio file metadata
    """
    if not storage_client:
        logger.error("Storage client not initialized")
        return []
    
    try:
        bucket = storage_client.get_bucket(GCS_CONFIG["bucket_name"])
        blobs = bucket.list_blobs(prefix=prefix)
        
        audio_files = []
        for blob in blobs:
            # Skip directories
            if blob.name.endswith('/'):
                continue
                
            # Extract metadata
            metadata = {
                "id": blob.name,
                "name": Path(blob.name).stem,
                "size": blob.size,
                "updated": blob.updated,
                "content_type": blob.content_type,
            }
            
            # Add custom metadata if available
            if blob.metadata:
                metadata.update(blob.metadata)
                
            audio_files.append(metadata)
            
        return audio_files
    except Exception as e:
        logger.error(f"Error listing audio files: {str(e)}")
        return []

def get_audio_file(file_id: str) -> Dict[str, Any]:
    """
    Get audio file metadata.
    
    Args:
        file_id: ID of the audio file
        
    Returns:
        Audio file metadata
    """
    if not storage_client:
        logger.error("Storage client not initialized")
        return {}
    
    try:
        bucket = storage_client.get_bucket(GCS_CONFIG["bucket_name"])
        blob = bucket.get_blob(file_id)
        
        if not blob:
            logger.error(f"Audio file {file_id} not found")
            return {}
            
        # Extract metadata
        metadata = {
            "id": blob.name,
            "name": Path(blob.name).stem,
            "size": blob.size,
            "updated": blob.updated,
            "content_type": blob.content_type,
        }
        
        # Add custom metadata if available
        if blob.metadata:
            metadata.update(blob.metadata)
            
        return metadata
    except Exception as e:
        logger.error(f"Error getting audio file {file_id}: {str(e)}")
        return {}

def download_audio_file(file_id: str) -> str:
    """
    Download audio file from GCS bucket.
    
    Args:
        file_id: ID of the audio file
        
    Returns:
        Path to downloaded file
    """
    if not storage_client:
        logger.error("Storage client not initialized")
        raise Exception("Storage client not initialized")
    
    try:
        bucket = storage_client.get_bucket(GCS_CONFIG["bucket_name"])
        blob = bucket.get_blob(file_id)
        
        if not blob:
            logger.error(f"Audio file {file_id} not found")
            raise FileNotFoundError(f"Audio file {file_id} not found")
            
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=Path(file_id).suffix)
        temp_path = temp_file.name
        temp_file.close()
        
        # Download to temporary file
        blob.download_to_filename(temp_path)
        
        return temp_path
    except Exception as e:
        logger.error(f"Error downloading audio file {file_id}: {str(e)}")
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
    Process audio file for playback.
    
    Args:
        file_id: ID of the audio file
        start_time: Start time in seconds
        end_time: End time in seconds
        speed: Playback speed
        repeat: Whether to repeat the audio
        
    Returns:
        Streaming response with audio data
    """
    try:
        # Download audio file
        file_path = download_audio_file(file_id)
        
        # Load audio file
        audio = AudioSegment.from_file(file_path)
        
        # Process audio
        if start_time > 0:
            audio = audio[start_time * 1000:]
            
        if end_time is not None:
            audio = audio[:end_time * 1000]
            
        # Apply speed
        if speed != 1.0:
            # This is a placeholder for speed adjustment
            # In a real implementation, we would use a library like librosa
            pass
            
        # Create temporary file for processed audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_path = temp_file.name
        temp_file.close()
        
        # Export processed audio
        audio.export(temp_path, format="mp3")
        
        # Return file path
        return temp_path
    except Exception as e:
        logger.error(f"Error processing audio file {file_id}: {str(e)}")
        raise
