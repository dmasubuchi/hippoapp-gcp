#!/bin/bash

# Script to update Cloud Run service IAM policy

# Set variables
PROJECT_ID="lucid-inquiry-453823-b0"
REGION="us-west1"
SERVICE_NAME="hippoapp"

echo "Updating Cloud Run service IAM policy..."

# Add IAM policy binding to allow unauthenticated access
echo "Adding IAM policy binding for allUsers..."
gcloud run services add-iam-policy-binding $SERVICE_NAME \
  --region=$REGION \
  --member="allUsers" \
  --role="roles/run.invoker"

echo "Cloud Run service IAM policy updated successfully!"
echo "You can now access the service at: https://$SERVICE_NAME-546tyu2ata-uw.a.run.app"
