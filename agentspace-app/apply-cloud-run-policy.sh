#!/bin/bash

# Script to apply Cloud Run policy for public access

# Set variables
PROJECT_ID="lucid-inquiry-453823-b0"
REGION="us-west1"
SERVICE_NAME="hippoapp"

echo "Applying Cloud Run policy for public access..."

# Create IAM policy file
cat > policy.yaml << 'EOF'
bindings:
- members:
  - allUsers
  role: roles/run.invoker
etag: ACAB
EOF

# Apply the IAM policy to the Cloud Run service
echo "Applying IAM policy to allow unauthenticated access..."
gcloud run services set-iam-policy $SERVICE_NAME \
  --region=$REGION \
  policy.yaml

echo "Cloud Run policy applied successfully!"
echo "You can now access the service at: https://$SERVICE_NAME-546tyu2ata-uw.a.run.app"
