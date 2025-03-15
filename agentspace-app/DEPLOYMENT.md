# Cloud Run Deployment Instructions

## Prerequisites
- Google Cloud SDK installed and configured
- Docker installed and configured
- Access to the GCP project: `lucid-inquiry-453823-b0`
- Service account with necessary permissions

## Deployment Steps

1. **Authenticate with Google Cloud**
   ```bash
   gcloud auth login
   gcloud config set project lucid-inquiry-453823-b0
   ```

2. **Build and Push the Docker Image**
   ```bash
   cd /path/to/hippoapp-gcp/agentspace-app
   docker build -t gcr.io/lucid-inquiry-453823-b0/hippoapp:latest .
   docker push gcr.io/lucid-inquiry-453823-b0/hippoapp:latest
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy hippoapp \
     --image gcr.io/lucid-inquiry-453823-b0/hippoapp:latest \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated \
     --service-account hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com
   ```

4. **Verify Deployment**
   - Access the application at the URL provided by Cloud Run
   - Test the multilingual audio player functionality
   - Verify that the application can access audio files from the GCP bucket

## Environment Variables
The following environment variables are required for the application:
- `GCP_PROJECT_ID`: lucid-inquiry-453823-b0
- `GCP_STORAGE_BUCKET`: language-learning-audio
- `GOOGLE_APPLICATION_CREDENTIALS`: /app/credentials/service-account-key.json

## Troubleshooting
- If the application cannot access the GCP bucket, verify the service account permissions
- If the application fails to start, check the Cloud Run logs for errors
- For local testing, use the provided `deploy-to-cloud-run.sh` script
