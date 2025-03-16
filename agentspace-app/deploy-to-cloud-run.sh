#!/bin/bash
# Deploy the Hippo Family Club application to Cloud Run

set -e

# Set variables
export PROJECT_ID=lucid-inquiry-453823-b0
export REGION=us-west1
export SERVICE_NAME=hippoapp
export SERVICE_ACCOUNT=hippoapp-service@$PROJECT_ID.iam.gserviceaccount.com

# Check if service account key exists
if [ ! -f "credentials/service-account-key.json" ]; then
    echo "Service account key not found. Creating a mock key for testing..."
    mkdir -p credentials
    cp credentials/service-account-key-template.json credentials/service-account-key.json
fi

# Build the container image
echo "Building container image..."
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .

# Push the image to Container Registry
echo "Pushing image to Container Registry..."
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --service-account $SERVICE_ACCOUNT \
    --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID,GCP_STORAGE_BUCKET=language-learning-audio"

echo "Deployment completed successfully!"
echo "Application URL: $(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format='value(status.url)')"
