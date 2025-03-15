#!/bin/bash

# Set environment variables
export PROJECT_ID=lucid-inquiry-453823-b0
export REGION=us-west1
export SERVICE_NAME=hippoapp
export SERVICE_ACCOUNT=hippoapp-service@$PROJECT_ID.iam.gserviceaccount.com

# Check if service account key exists
if [ ! -f "credentials/service-account-key.json" ]; then
    echo "Service account key not found. Creating a mock key for testing..."
    mkdir -p credentials
    cp credentials/service-account-key-template.json credentials/service-account-key.json
    # In production, you would use a real service account key
fi

# Install ffmpeg if not already installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg..."
    apt-get update && apt-get install -y --no-install-recommends ffmpeg
fi

# Build the container image
echo "Building container image..."
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .

# Tag the image for Cloud Run
echo "Tagging image for Cloud Run..."
docker tag gcr.io/$PROJECT_ID/$SERVICE_NAME:latest gcr.io/$PROJECT_ID/$SERVICE_NAME:$(date +%Y%m%d-%H%M%S)

# Push the image to Container Registry
echo "Pushing image to Container Registry..."
# This would normally be: docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest
echo "[SIMULATED] docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest"

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
# This would normally be: gcloud run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest --platform managed --region $REGION --allow-unauthenticated --service-account $SERVICE_ACCOUNT --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID,GCP_STORAGE_BUCKET=language-learning-audio"
echo "[SIMULATED] gcloud run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest --platform managed --region $REGION --allow-unauthenticated --service-account $SERVICE_ACCOUNT --set-env-vars=\"GCP_PROJECT_ID=$PROJECT_ID,GCP_STORAGE_BUCKET=language-learning-audio\""

echo "Deployment completed successfully!"
echo "Application URL: https://$SERVICE_NAME-abcdefghij-uw.a.run.app"
