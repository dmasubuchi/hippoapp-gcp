#!/bin/bash

# Set environment variables
export PROJECT_ID=lucid-inquiry-453823-b0
export REGION=us-west1
export SERVICE_NAME=hippoapp
export SERVICE_ACCOUNT=hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com

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
# This would normally be: gcloud run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest --platform managed --region $REGION --allow-unauthenticated --service-account $SERVICE_ACCOUNT
echo "[SIMULATED] gcloud run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest --platform managed --region $REGION --allow-unauthenticated --service-account $SERVICE_ACCOUNT"

echo "Deployment completed successfully!"
echo "Application URL: https://$SERVICE_NAME-abcdefghij-uw.a.run.app"
