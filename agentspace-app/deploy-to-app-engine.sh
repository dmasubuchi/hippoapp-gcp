#!/bin/bash
set -e

# Configuration
export PROJECT_ID=lucid-inquiry-453823-b0
export REGION=us-west1

# Check if App Engine application exists
echo "Checking if App Engine application exists..."
if ! gcloud app describe --project=$PROJECT_ID &>/dev/null; then
    echo "Creating App Engine application in region $REGION..."
    gcloud app create --project=$PROJECT_ID --region=$REGION
else
    echo "App Engine application already exists."
fi

# Deploy to App Engine
echo "Deploying to App Engine..."
gcloud app deploy app.yaml --project=$PROJECT_ID --quiet

# Display the deployed URL
echo "Deployment completed successfully!"
echo "Application URL: https://$PROJECT_ID.uw.r.appspot.com"
