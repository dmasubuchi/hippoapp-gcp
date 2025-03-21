# Hippo Family Club - Multilingual Audio Player

A multilingual audio player application for language learning, built with FastAPI and Google Cloud Platform services.

## Features

- MP3 audio playback with time-tagged sentences
- Language switching with synchronized sentence highlighting
- Responsive design for desktop and mobile devices
- Integration with Google Cloud Storage for audio files

## Prerequisites

- Python 3.9+
- Google Cloud Platform account
- Google Cloud Storage bucket with audio files
- Service account with appropriate permissions

## Local Development Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure Google Cloud credentials:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   ```

3. Update the configuration in `config.py` with your specific settings.

4. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

5. Access the application at http://localhost:8080

## Deployment to Google Cloud Run

### Option 1: Using gcloud CLI

1. Install and initialize the Google Cloud SDK:
   ```
   gcloud init
   gcloud auth login
   ```

2. Build and deploy the application:
   ```
   gcloud builds submit --tag gcr.io/PROJECT_ID/hippoapp
   gcloud run deploy hippoapp --image gcr.io/PROJECT_ID/hippoapp --platform managed --region us-west1 --allow-unauthenticated
   ```

### Option 2: Using Cloud Build

1. Configure the `cloudbuild.yaml` file with your project-specific settings.

2. Trigger a build:
   ```
   gcloud builds submit --config=cloudbuild.yaml
   ```

## Service Account Requirements

The application requires a service account with the following permissions:
- Storage Object Viewer (`roles/storage.objectViewer`) for the audio bucket
- Cloud Run Service Agent (`roles/run.serviceAgent`) for deployment

## Environment Variables

The following environment variables can be configured:

- `DEBUG`: Enable debug mode (default: False)
- `PORT`: Port to run the application on (default: 8080)
- `GCP_PROJECT_ID`: Google Cloud project ID
- `GCP_STORAGE_BUCKET`: Google Cloud Storage bucket name
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account key file

## Project Structure

- `app/`: Application code
  - `main.py`: FastAPI application entry point
  - `utils.py`: Utility functions for GCP services
  - `static/`: Static assets (CSS, JavaScript)
  - `templates/`: HTML templates
- `config.py`: Application configuration
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
- `cloudbuild.yaml`: Cloud Build configuration
