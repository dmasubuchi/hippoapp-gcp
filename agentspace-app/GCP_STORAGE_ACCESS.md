# GCP Storage Access Implementation

This document describes the implementation of GCP storage access in the Hippo Family Club application.

## Overview

The application uses Google Cloud Storage to store and retrieve audio files for the multilingual audio player. The implementation supports both production and local development environments, with proper error handling and mock data support.

## Key Components

### 1. GCP Service Initialization

The `setup_gcp_services()` function in `utils.py` initializes the GCP storage client with the appropriate credentials:

- In production, it uses the service account key specified in the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- In development mode, it attempts to use default credentials or falls back to mock data

### 2. Mock Data Support

For local development without GCP credentials, the application provides mock data:

- Audio file metadata is generated with appropriate language codes
- Audio playback uses generated tones with different pitches for different languages
- Error handling gracefully falls back to mock data when GCP services are unavailable

### 3. Environment Configuration

The application uses environment variables to configure its behavior:

- `DEBUG`: Enables debug mode with mock data support
- `GCP_PROJECT_ID`: The GCP project ID
- `GCP_STORAGE_BUCKET`: The GCP storage bucket name
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to the service account key file

### 4. Service Account Management

The application includes scripts to manage service accounts:

- `create-service-account.sh`: Creates a service account and grants it the necessary permissions
- `test-storage-access.sh`: Tests access to the GCP storage bucket

## Testing

The application can be tested locally using:

```bash
export DEBUG=True
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

This will start the application in debug mode with mock data support, allowing testing without GCP credentials.

## Deployment

For deployment to GCP, the application supports both App Engine and Cloud Run:

- App Engine: Use the `deploy-to-app-engine.sh` script
- Cloud Run: Use the `deploy-to-cloud-run.sh` script

Both deployment options require proper GCP authentication and service account setup.
