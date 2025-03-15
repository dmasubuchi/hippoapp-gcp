"""
Utility functions for the Hippo Family Club language learning app.
"""
import os
import logging
import tempfile
from pathlib import Path
import sys
from google.cloud import storage
from fastapi.responses import StreamingResponse
from pydub import AudioSegment
import io

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import GCS_CONFIG, PLAYBACK_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global clients
storage_client = None

def setup_gcp_services():
    """Set up Google Cloud Platform services."""
    global storage_client
    
    try:
        # Initialize Storage client
        storage_client = storage.Client()
        logger.info("GCP services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing GCP services: {str(e)}")
        raise

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
        }
        
        # Add custom metadata if available
        if blob.metadata:
            metadata.update(blob.metadata)
        
        return metadata
    except Exception as e:
        logger.error(f"Error getting audio file {file_id}: {str(e)}")
        raise

def download_audio_file(file_id):
    """
    Download audio file from Google Cloud Storage.
    
    Args:
        file_id: ID of the audio file
        
    Returns:
        str: Path to the downloaded file
    """
    global storage_client
    
    if storage_client is None:
        setup_gcp_services()
    
    try:
        # Get bucket
        bucket = storage_client.bucket(GCS_CONFIG["bucket_name"])
        
        # List blobs with prefix
        blobs = list(bucket.list_blobs(prefix=f"audio/{file_id}"))
        
        if not blobs:
            raise ValueError(f"Audio file {file_id} not found")
        
        # Get the first matching blob
        blob = blobs[0]
        
        # Create cache directory if it doesn't exist
        os.makedirs(PLAYBACK_CONFIG["cache_directory"], exist_ok=True)
        
        # Download to cache
        file_name = os.path.basename(blob.name)
        local_path = os.path.join(PLAYBACK_CONFIG["cache_directory"], file_name)
        
        # Check if file already exists in cache
        if os.path.exists(local_path) and os.path.getsize(local_path) == blob.size:
            logger.info(f"Using cached file {local_path}")
        else:
            logger.info(f"Downloading {blob.name} to {local_path}")
            blob.download_to_filename(local_path)
        
        return local_path
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
        StreamingResponse: Streaming response with audio data
    """
    try:
        # Download audio file
        local_path = download_audio_file(file_id)
        
        # Get file extension
        file_ext = os.path.splitext(local_path)[1].lower().replace(".", "")
        
        # Load audio file
        if file_ext == "mp3":
            audio = AudioSegment.from_mp3(local_path)
        elif file_ext == "wav":
            audio = AudioSegment.from_wav(local_path)
        elif file_ext == "ogg":
            audio = AudioSegment.from_ogg(local_path)
        elif file_ext == "flac":
            audio = AudioSegment.from_file(local_path, format="flac")
        else:
            raise ValueError(f"Unsupported audio format: {file_ext}")
        
        # Apply start and end times
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000) if end_time is not None else len(audio)
        
        audio = audio[start_ms:end_ms]
        
        # Apply speed adjustment
        if speed != 1.0:
            # Check if speed is within allowed range
            if speed < PLAYBACK_CONFIG["speed_range"][0] or speed > PLAYBACK_CONFIG["speed_range"][1]:
                raise ValueError(f"Speed {speed} is outside allowed range {PLAYBACK_CONFIG['speed_range']}")
            
            # Adjust speed (this is a simple implementation, more sophisticated methods exist)
            audio = audio.speedup(playback_speed=speed)
        
        # Apply repeat if needed
        if repeat:
            audio = audio * 3  # Repeat 3 times
        
        # Export to bytes
        buffer = io.BytesIO()
        audio.export(buffer, format=file_ext)
        buffer.seek(0)
        
        # Create streaming response
        return StreamingResponse(
            buffer, 
            media_type=f"audio/{file_ext}",
            headers={"Content-Disposition": f"attachment; filename={file_id}.{file_ext}"}
        )
    except Exception as e:
        logger.error(f"Error processing audio playback for {file_id}: {str(e)}")
        raise
