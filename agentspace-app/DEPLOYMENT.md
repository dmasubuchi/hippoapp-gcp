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

2. **Set up Service Account Key (Securely)**
   - Create a service account key in the GCP Console
   - Download the key file and store it securely
   - Never commit the key file to the repository
   - Set the environment variable to point to the key file:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
     ```

3. **Build and Push the Docker Image**
   ```bash
   cd /path/to/hippoapp-gcp/agentspace-app
   docker build -t gcr.io/lucid-inquiry-453823-b0/hippoapp:latest .
   docker push gcr.io/lucid-inquiry-453823-b0/hippoapp:latest
   ```

4. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy hippoapp \
     --image gcr.io/lucid-inquiry-453823-b0/hippoapp:latest \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated \
     --service-account hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com \
     --set-env-vars="GCP_PROJECT_ID=lucid-inquiry-453823-b0,GCP_STORAGE_BUCKET=language-learning-audio"
   ```

5. **Set up Secret Management (Recommended)**
   ```bash
   # Create a secret for the service account key
   gcloud secrets create hippoapp-sa-key --data-file=/path/to/service-account-key.json
   
   # Grant access to the service account
   gcloud secrets add-iam-policy-binding hippoapp-sa-key \
     --member=serviceAccount:hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com \
     --role=roles/secretmanager.secretAccessor
   
   # Update the Cloud Run service to use the secret
   gcloud run services update hippoapp \
     --region=us-west1 \
     --update-secrets=GOOGLE_APPLICATION_CREDENTIALS=hippoapp-sa-key:latest
   ```

6. **Verify Deployment**
   - Access the application at the URL provided by Cloud Run
   - Test the multilingual audio player functionality
   - Verify that the application can access audio files from the GCP bucket

## Environment Variables
The following environment variables are required for the application:
- `GCP_PROJECT_ID`: Project ID for Google Cloud
- `GCP_STORAGE_BUCKET`: Name of the GCS bucket containing audio files
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to the service account key file

## Security Best Practices
- Never store service account keys in the repository
- Use Secret Manager for storing sensitive credentials
- Limit service account permissions to only what is necessary
- Regularly rotate service account keys
- Use environment variables for configuration

## Troubleshooting
- If the application cannot access the GCP bucket, verify the service account permissions
- If the application fails to start, check the Cloud Run logs for errors
- For local testing, use the provided `deploy-to-cloud-run.sh` script
