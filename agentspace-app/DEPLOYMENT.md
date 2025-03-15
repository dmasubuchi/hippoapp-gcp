# Cloud Run Deployment Instructions

## Prerequisites
- Google Cloud SDK installed and configured
- Docker installed and configured
- Access to the GCP project: `lucid-inquiry-453823-b0`
- Service account with necessary permissions

## Important Notes
- The application requires ffmpeg for audio processing
- The service account key must be properly formatted JSON
- Environment variables must be correctly configured

## Troubleshooting
- If you encounter "Invalid control character" errors, check the service account key format
- If audio processing doesn't work, verify ffmpeg is installed in the container
- If the application can't access GCP resources, check the service account permissions
- If the deployment URL shows nothing, check the Cloud Run logs for startup errors
