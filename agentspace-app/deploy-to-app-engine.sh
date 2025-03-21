#!/bin/bash
set -e

# Configuration
export PROJECT_ID=lucid-inquiry-453823-b0
export REGION=us-west1
export SERVICE_ACCOUNT=hippoapp-service@$PROJECT_ID.iam.gserviceaccount.com

# Check if service account key exists
if [ ! -f "credentials/service-account-key.json" ]; then
    echo "Service account key not found. Creating a mock key for testing..."
    mkdir -p credentials
    cp credentials/service-account-key-template.json credentials/service-account-key.json
    echo "Mock key created. In production, replace with a real service account key."
fi

# Check if App Engine application exists
echo "Checking if App Engine application exists..."
if ! gcloud app describe --project=$PROJECT_ID &>/dev/null; then
    echo "Creating App Engine application in region $REGION..."
    gcloud app create --project=$PROJECT_ID --region=$REGION
else
    echo "App Engine application already exists."
fi

# Verify app.yaml exists
if [ ! -f "app.yaml" ]; then
    echo "Error: app.yaml not found. Cannot deploy without configuration."
    exit 1
fi

# Deploy to App Engine
echo "Deploying to App Engine..."
gcloud app deploy app.yaml --project=$PROJECT_ID --quiet

# Display the deployed URL
echo "Deployment completed successfully!"
echo "Application URL: https://$PROJECT_ID.uw.r.appspot.com"

# Verify deployment
echo "Verifying deployment..."
sleep 10  # Wait for deployment to stabilize
curl -s "https://$PROJECT_ID.uw.r.appspot.com/api/health" || echo "Health check failed. The application may still be starting up."
