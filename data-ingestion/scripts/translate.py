"""
Translation utilities using Google Cloud Translation API.
"""
import json
import logging
from google.cloud import translate_v2 as translate
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import TRANSLATION_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def translate_text(text, source_language=None, target_language="en"):
    """
    Translate text using Google Cloud Translation API.
    
    Args:
        text (str): Text to translate
        source_language (str, optional): Source language code
        target_language (str): Target language code
        
    Returns:
        dict: Translation result
    """
    try:
        # Create translation client
        client = translate.Client()
        
        # Perform translation
        result = client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
            format_="text"
        )
        
        translation = {
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"] if source_language is None else source_language,
            "target_language": target_language,
            "model": result.get("model", "base")
        }
        
        logger.info(f"Translated text from {translation['source_language']} to {target_language}")
        return translation
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        return None

def translate_file(input_file, source_language=None, target_language="en"):
    """
    Translate text from a file.
    
    Args:
        input_file (str): Path to the input file
        source_language (str, optional): Source language code
        target_language (str): Target language code
        
    Returns:
        dict: Translation result
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return translate_text(text, source_language, target_language)
    except Exception as e:
        logger.error(f"Error reading input file: {str(e)}")
        return None

def translate_json_file(input_file, text_field, source_language=None, target_language="en"):
    """
    Translate a specific field in a JSON file.
    
    Args:
        input_file (str): Path to the JSON file
        text_field (str): Field containing text to translate
        source_language (str, optional): Source language code
        target_language (str): Target language code
        
    Returns:
        dict: Original JSON with translated field added
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract text to translate
        if text_field not in data:
            logger.error(f"Field '{text_field}' not found in JSON file")
            return None
        
        text = data[text_field]
        
        # Translate text
        translation = translate_text(text, source_language, target_language)
        if not translation:
            return None
        
        # Add translation to data
        translated_field = f"{text_field}_translated_{target_language}"
        data[translated_field] = translation["translated_text"]
        
        return data
    except Exception as e:
        logger.error(f"Error processing JSON file: {str(e)}")
        return None

def save_translation(translation, output_file):
    """
    Save translation results to a file.
    
    Args:
        translation (dict): Translation results
        output_file (str): Path to save the results
        
    Returns:
        bool: Success status
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            if isinstance(translation, dict):
                json.dump(translation, f, ensure_ascii=False, indent=2)
            else:
                f.write(translation)
        logger.info(f"Translation saved to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving translation: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Translate text using Google Cloud Translation API")
    parser.add_argument("--text", "-t", help="Text to translate")
    parser.add_argument("--file", "-f", help="File containing text to translate")
    parser.add_argument("--json", "-j", help="JSON file to translate")
    parser.add_argument("--field", help="Field in JSON file to translate")
    parser.add_argument("--source", "-s", help="Source language code")
    parser.add_argument("--target", "-tg", default="en", help="Target language code")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    result = None
    
    if args.text:
        result = translate_text(args.text, args.source, args.target)
    elif args.file:
        result = translate_file(args.file, args.source, args.target)
    elif args.json and args.field:
        result = translate_json_file(args.json, args.field, args.source, args.target)
    else:
        parser.print_help()
        sys.exit(1)
    
    if result:
        if args.output:
            save_translation(result, args.output)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
