"""
Metadata extraction utilities for audio files.
"""
import os
import json
import logging
from pathlib import Path
import sys
import librosa
import soundfile as sf
from pydub import AudioSegment
from google.cloud import storage
import tempfile

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import METADATA_SCHEMA, AUDIO_PROCESSING_CONFIG, GCS_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_from_gcs(gcs_uri, local_path=None):
    """
    Download a file from Google Cloud Storage.
    
    Args:
        gcs_uri (str): GCS URI of the file to download
        local_path (str, optional): Local path to save the file
        
    Returns:
        str: Path to the downloaded file
    """
    if not gcs_uri.startswith("gs://"):
        logger.error(f"Invalid GCS URI: {gcs_uri}")
        return None
    
    try:
        # Parse bucket and blob names
        bucket_name = gcs_uri.split("/")[2]
        blob_name = "/".join(gcs_uri.split("/")[3:])
        
        # Create storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        # Create temporary file if local path not provided
        if local_path is None:
            temp_dir = tempfile.mkdtemp()
            file_name = os.path.basename(blob_name)
            local_path = os.path.join(temp_dir, file_name)
        
        # Download file
        blob.download_to_filename(local_path)
        logger.info(f"Downloaded {gcs_uri} to {local_path}")
        
        return local_path
    except Exception as e:
        logger.error(f"Error downloading from GCS: {str(e)}")
        return None

def extract_audio_metadata(audio_file_path):
    """
    Extract metadata from an audio file.
    
    Args:
        audio_file_path (str): Path to the audio file or GCS URI
        
    Returns:
        dict: Extracted metadata
    """
    # Check if the file is a GCS URI
    if audio_file_path.startswith("gs://"):
        local_path = download_from_gcs(audio_file_path)
        if not local_path:
            return None
    else:
        local_path = audio_file_path
    
    try:
        # Get file extension
        file_ext = os.path.splitext(local_path)[1].lower().replace(".", "")
        
        # Check if format is supported
        if file_ext not in AUDIO_PROCESSING_CONFIG["supported_formats"]:
            logger.error(f"Unsupported audio format: {file_ext}")
            return None
        
        # Extract basic metadata
        metadata = {
            "file_name": os.path.basename(local_path),
            "file_size_bytes": os.path.getsize(local_path),
            "file_format": file_ext,
        }
        
        # Extract audio properties using librosa
        y, sr = librosa.load(local_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        
        metadata.update({
            "duration": duration,
            "sample_rate": sr,
            "channels": 1 if len(y.shape) == 1 else y.shape[1],
        })
        
        # Get more detailed format info using soundfile
        sf_info = sf.info(local_path)
        metadata.update({
            "format_info": sf_info.format,
            "subtype_info": sf_info.subtype,
        })
        
        # Try to get more metadata using pydub for formats like MP3
        try:
            if file_ext == "mp3":
                audio = AudioSegment.from_mp3(local_path)
                metadata["channels"] = audio.channels
                metadata["frame_rate"] = audio.frame_rate
                metadata["frame_width"] = audio.frame_width
                metadata["frame_count"] = int(audio.frame_count())
            elif file_ext == "wav":
                audio = AudioSegment.from_wav(local_path)
                metadata["channels"] = audio.channels
                metadata["frame_rate"] = audio.frame_rate
                metadata["frame_width"] = audio.frame_width
                metadata["frame_count"] = int(audio.frame_count())
        except Exception as e:
            logger.warning(f"Could not extract additional metadata: {str(e)}")
        
        # Clean up temporary file if it was downloaded from GCS
        if audio_file_path.startswith("gs://") and os.path.dirname(local_path).startswith(tempfile.gettempdir()):
            os.remove(local_path)
            logger.info(f"Removed temporary file {local_path}")
        
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata: {str(e)}")
        
        # Clean up temporary file if it was downloaded from GCS
        if audio_file_path.startswith("gs://") and os.path.dirname(local_path).startswith(tempfile.gettempdir()):
            try:
                os.remove(local_path)
            except:
                pass
        
        return None

def validate_metadata(metadata, schema=None):
    """
    Validate metadata against the schema.
    
    Args:
        metadata (dict): Metadata to validate
        schema (dict, optional): Schema to validate against
        
    Returns:
        tuple: (is_valid, missing_fields, extra_fields)
    """
    if schema is None:
        schema = METADATA_SCHEMA
    
    required_fields = schema.get("required_fields", [])
    optional_fields = schema.get("optional_fields", [])
    
    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in metadata]
    
    # Check for extra fields
    all_allowed_fields = required_fields + optional_fields
    extra_fields = [field for field in metadata if field not in all_allowed_fields]
    
    is_valid = len(missing_fields) == 0
    
    return (is_valid, missing_fields, extra_fields)

def save_metadata(metadata, output_file):
    """
    Save metadata to a JSON file.
    
    Args:
        metadata (dict): Metadata to save
        output_file (str): Path to save the metadata
        
    Returns:
        bool: Success status
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        logger.info(f"Metadata saved to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving metadata: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract metadata from audio files")
    parser.add_argument("audio_file", help="Path to the audio file or GCS URI")
    parser.add_argument("--output", "-o", help="Output file path for JSON results")
    parser.add_argument("--validate", "-v", action="store_true", help="Validate metadata against schema")
    
    args = parser.parse_args()
    
    metadata = extract_audio_metadata(args.audio_file)
    
    if metadata:
        if args.validate:
            is_valid, missing, extra = validate_metadata(metadata)
            print(f"Validation: {'PASSED' if is_valid else 'FAILED'}")
            if missing:
                print(f"Missing required fields: {', '.join(missing)}")
            if extra:
                print(f"Extra fields: {', '.join(extra)}")
        
        if args.output:
            save_metadata(metadata, args.output)
        else:
            print(json.dumps(metadata, ensure_ascii=False, indent=2))
