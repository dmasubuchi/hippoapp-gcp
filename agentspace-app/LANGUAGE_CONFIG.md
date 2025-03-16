# Hippo Family Club Language Configuration

This document describes the language configuration for the Hippo Family Club multilingual audio player.

## Supported Languages

The application currently supports the following languages:

| Language Code | Language Name |
|--------------|---------------|
| en | English |
| ja | Japanese |
| fr | French |
| es | Spanish |
| de | German |
| zh | Chinese |
| ko | Korean |
| it | Italian |
| ru | Russian |
| pt | Portuguese |

## Language Detection

The application detects the language of an audio file based on its path. For example:

- `/audio/en/lesson1.mp3` - English
- `/audio/ja/lesson1.mp3` - Japanese
- `/audio/fr/lesson1.mp3` - French

## Adding New Languages

To add support for a new language:

1. Update the `LANGUAGE_CONFIG` dictionary in `config.py`
2. Add the language pattern to the `get_language_from_path` function in `utils.py`
3. Update the UI to display the new language option

## Language Switching

The application allows users to switch between languages while maintaining the same position in the audio content. This is achieved by:

1. Storing time mappings between sentences in different languages
2. When a user switches language, the application finds the corresponding sentence in the new language
3. The audio playback jumps to the start time of that sentence in the new language

## Mock Data for Development

In development mode, the application generates mock audio data for each language with different tones to simulate different languages:

- English: Medium pitch tones
- Japanese: Higher pitch tones
- French: Lower pitch tones

This allows for testing the language switching functionality without requiring actual audio files.
