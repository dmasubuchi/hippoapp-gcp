#!/bin/bash

# Create a service account key for development

# Set variables
PROJECT_ID="lucid-inquiry-453823-b0"
SERVICE_ACCOUNT="hippoapp-service@${PROJECT_ID}.iam.gserviceaccount.com"
KEY_FILE="credentials/service-account-key.json"

# Create credentials directory if it doesn't exist
mkdir -p credentials

# Check if service account exists
if ! gcloud iam service-accounts describe ${SERVICE_ACCOUNT} &>/dev/null; then
    echo "Creating service account..."
    gcloud iam service-accounts create hippoapp-service \
        --display-name="Hippo App Service Account" \
        --project=${PROJECT_ID}
fi

# Grant storage permissions to the service account
echo "Granting storage permissions..."
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/storage.objectViewer"

# Create a key for the service account
echo "Creating service account key..."
gcloud iam service-accounts keys create ${KEY_FILE} \
    --iam-account=${SERVICE_ACCOUNT}

echo "Service account key created at ${KEY_FILE}"
echo "Set the following environment variable:"
echo "export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/${KEY_FILE}"
