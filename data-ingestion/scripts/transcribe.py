"""
Audio transcription utilities using Google Cloud Speech-to-Text.
"""
import os
import json
from google.cloud import speech
from google.cloud import storage
import logging
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import SPEECH_TO_TEXT_CONFIG, GCS_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_audio_to_gcs(local_file_path, bucket_name=None):
    """
    Upload an audio file to Google Cloud Storage.
    
    Args:
        local_file_path (str): Path to the local audio file
        bucket_name (str, optional): GCS bucket name. Defaults to config value.
        
    Returns:
        str: GCS URI of the uploaded file
    """
    if bucket_name is None:
        bucket_name = GCS_CONFIG["bucket_name"]
    
    try:
        # Create storage client
        storage_client = storage.Client()
        
        # Get or create bucket
        try:
            bucket = storage_client.get_bucket(bucket_name)
        except Exception:
            logger.info(f"Bucket {bucket_name} not found, creating it...")
            bucket = storage_client.create_bucket(bucket_name)
        
        # Upload file
        file_name = os.path.basename(local_file_path)
        blob = bucket.blob(f"audio/{file_name}")
        blob.upload_from_filename(local_file_path)
        
        gcs_uri = f"gs://{bucket_name}/audio/{file_name}"
        logger.info(f"File {local_file_path} uploaded to {gcs_uri}")
        
        return gcs_uri
    except Exception as e:
        logger.error(f"Error uploading file to GCS: {str(e)}")
        return None

def transcribe_audio_file(audio_file_path, language_code=None, enable_speaker_diarization=True):
    """
    Transcribe an audio file using Google Cloud Speech-to-Text.
    
    Args:
        audio_file_path (str): Path to the local audio file or GCS URI
        language_code (str, optional): Language code for transcription
        enable_speaker_diarization (bool): Whether to enable speaker separation
        
    Returns:
        dict: Transcription results
    """
    # Set default language code if not provided
    if language_code is None:
        language_code = SPEECH_TO_TEXT_CONFIG["language_codes"][0]  # Default to first language
    
    # Check if the file is already a GCS URI
    if not audio_file_path.startswith("gs://"):
        # Upload to GCS first
        gcs_uri = upload_audio_to_gcs(audio_file_path)
        if not gcs_uri:
            return None
    else:
        gcs_uri = audio_file_path
    
    try:
        # Create speech client
        client = speech.SpeechClient()
        
        # Configure audio
        audio = speech.RecognitionAudio(uri=gcs_uri)
        
        # Configure recognition
        diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=enable_speaker_diarization,
            min_speaker_count=1,
            max_speaker_count=SPEECH_TO_TEXT_CONFIG.get("diarization_speaker_count", 3)
        )
        
        config = speech.RecognitionConfig(
            encoding=getattr(speech.RecognitionConfig.AudioEncoding, SPEECH_TO_TEXT_CONFIG["audio_encoding"]),
            sample_rate_hertz=SPEECH_TO_TEXT_CONFIG["sample_rate_hertz"],
            language_code=language_code,
            enable_automatic_punctuation=True,
            diarization_config=diarization_config,
            enable_word_time_offsets=True,
        )
        
        # Perform long-running recognition
        logger.info(f"Starting transcription for {gcs_uri} in language {language_code}")
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=90)
        
        # Process results
        result = {
            "transcripts": [],
            "speakers": {},
            "metadata": {
                "language_code": language_code,
                "audio_uri": gcs_uri,
                "duration": None  # Will be set from the response
            }
        }
        
        # Extract transcript with speaker tags
        for i, res in enumerate(response.results):
            alternative = res.alternatives[0]
            transcript = alternative.transcript
            
            # Add to full transcripts
            result["transcripts"].append({
                "text": transcript,
                "confidence": alternative.confidence
            })
            
            # Process speaker tags if available
            if res.alternatives[0].words:
                for word_info in res.alternatives[0].words:
                    speaker_tag = word_info.speaker_tag
                    word = word_info.word
                    start_time = word_info.start_time.total_seconds()
                    end_time = word_info.end_time.total_seconds()
                    
                    # Update duration if this is the latest end time
                    if result["metadata"]["duration"] is None or end_time > result["metadata"]["duration"]:
                        result["metadata"]["duration"] = end_time
                    
                    # Add to speaker dictionary
                    if speaker_tag not in result["speakers"]:
                        result["speakers"][speaker_tag] = []
                    
                    result["speakers"][speaker_tag].append({
                        "word": word,
                        "start_time": start_time,
                        "end_time": end_time
                    })
        
        logger.info(f"Transcription completed with {len(result['speakers'])} speakers detected")
        return result
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return None

def transcribe_multilingual(audio_file_path, language_codes=None):
    """
    Transcribe audio in multiple languages.
    
    Args:
        audio_file_path (str): Path to the local audio file or GCS URI
        language_codes (list, optional): List of language codes to transcribe in
        
    Returns:
        dict: Transcription results for each language
    """
    if language_codes is None:
        language_codes = SPEECH_TO_TEXT_CONFIG["language_codes"]
    
    results = {}
    
    for language_code in language_codes:
        logger.info(f"Transcribing in {language_code}")
        result = transcribe_audio_file(audio_file_path, language_code)
        if result:
            results[language_code] = result
    
    return results

def save_transcription(transcription, output_file):
    """
    Save transcription results to a JSON file.
    
    Args:
        transcription (dict): Transcription results
        output_file (str): Path to save the results
        
    Returns:
        bool: Success status
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transcription, f, ensure_ascii=False, indent=2)
        logger.info(f"Transcription saved to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving transcription: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcribe audio files using Google Cloud Speech-to-Text")
    parser.add_argument("audio_file", help="Path to the audio file or GCS URI")
    parser.add_argument("--output", "-o", help="Output file path for JSON results")
    parser.add_argument("--language", "-l", help="Language code for transcription")
    parser.add_argument("--multilingual", "-m", action="store_true", help="Perform multilingual transcription")
    parser.add_argument("--no-diarization", action="store_true", help="Disable speaker diarization")
    
    args = parser.parse_args()
    
    if args.multilingual:
        results = transcribe_multilingual(args.audio_file)
    else:
        results = transcribe_audio_file(
            args.audio_file, 
            language_code=args.language,
            enable_speaker_diarization=not args.no_diarization
        )
    
    if results:
        if args.output:
            save_transcription(results, args.output)
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
