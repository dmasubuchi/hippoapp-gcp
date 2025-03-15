# Data Ingestion Module

This module handles the ingestion, processing, and management of Hippo Family Club multilingual audio sources.

## Features

- Audio file ingestion and storage in Google Cloud Storage
- Metadata extraction and management
- Audio transcription using Google Cloud Speech-to-Text
- Translation services using Google Cloud Translation API
- Character voice separation and tagging

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure Google Cloud credentials:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   ```

3. Update the configuration in `config.py` with your specific settings.

## Usage

### Transcribe Audio

```python
from scripts.transcribe import transcribe_audio

result = transcribe_audio("path/to/audio.mp3", language_code="en-US")
print(result)
```

### Extract Metadata

```python
from scripts.metadata import extract_metadata

metadata = extract_metadata("path/to/audio.mp3")
print(metadata)
```

### Translate Text

```python
from scripts.translate import translate_text

translated = translate_text("Hello world", source_language="en", target_language="ja")
print(translated)
```

## Scripts

- `transcribe.py`: Audio transcription using Google Cloud Speech-to-Text
- `translate.py`: Text translation using Google Cloud Translation API
- `metadata.py`: Metadata extraction from audio files
