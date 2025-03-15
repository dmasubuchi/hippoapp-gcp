# Agentspace App Module

This module provides the Agentspace-powered language learning application for Hippo Family Club.

## Features

- Multilingual audio playback with advanced controls
- AI-powered learning support through Agentspace agents
- Personalized learning experiences
- Role-playing and pronunciation practice
- Progress tracking and learning optimization

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

### Start the Application

```
python app/main.py
```

### Configure Agents

Edit the agent configuration files in the `agents/` directory to customize the learning experience.

## Components

- `app/main.py`: Main application entry point
- `app/utils.py`: Utility functions for the application
- `agents/learning_agent/`: Configuration for the learning support agent
