# Service Account Configuration for Cloud Run Deployment

## Service Account Details
- **Name**: hippoapp-service
- **Email**: hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com
- **Project ID**: lucid-inquiry-453823-b0

## Required Permissions
- Storage Object Viewer (`roles/storage.objectViewer`) for the audio bucket
- Cloud Run Service Agent (`roles/run.serviceAgent`) for deployment

## Environment Variables
- `GCP_PROJECT_ID`: lucid-inquiry-453823-b0
- `GCP_STORAGE_BUCKET`: language-learning-audio
- `GOOGLE_APPLICATION_CREDENTIALS`: /app/credentials/service-account-key.json

## Deployment Instructions
1. Ensure the service account has the necessary permissions
2. Create a service account key and download it
3. Set up the environment variables in Cloud Run
4. Deploy the application using Cloud Build

## Security Considerations
- The service account key should be kept secure and not committed to the repository
- Use Cloud Run's built-in secret management for storing sensitive credentials
- Limit the service account permissions to only what is necessary
