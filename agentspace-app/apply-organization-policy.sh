#!/bin/bash
# Apply organization policy to allow unauthenticated access to Cloud Run

set -e

# Set variables
export PROJECT_ID=lucid-inquiry-453823-b0
export REGION=us-west1
export SERVICE_NAME=hippoapp

# Apply the organization policy
echo "Applying organization policy to allow unauthenticated access to Cloud Run..."
gcloud org-policies set-policy cloud-run-policy.yaml

# Verify the policy
echo "Verifying organization policy..."
gcloud org-policies describe iam.allowedPolicyMemberDomains --project=$PROJECT_ID

# Update the Cloud Run service IAM policy
echo "Updating Cloud Run service IAM policy..."
gcloud run services set-iam-policy $SERVICE_NAME --region=$REGION policy.yaml

# Verify the service URL
echo "Verifying service URL..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format='value(status.url)')
echo "Service URL: $SERVICE_URL"

# Test the service
echo "Testing service endpoints..."
curl -s $SERVICE_URL/api/health
echo ""
curl -s $SERVICE_URL/api/languages
echo ""

echo "Organization policy applied successfully."
