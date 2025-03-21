#!/bin/bash

# Test GCP storage access

# Set variables
BUCKET_NAME="language-learning-audio"

# Check if gsutil is installed
if ! command -v gsutil &>/dev/null; then
    echo "gsutil is not installed. Please install the Google Cloud SDK."
    exit 1
fi

# Check if authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &>/dev/null; then
    echo "Not authenticated with GCP. Please run 'gcloud auth login'."
    exit 1
fi

# Check if bucket exists
if ! gsutil ls gs://${BUCKET_NAME} &>/dev/null; then
    echo "Bucket ${BUCKET_NAME} does not exist or you don't have access to it."
    exit 1
fi

# List files in the bucket
echo "Files in bucket ${BUCKET_NAME}:"
gsutil ls gs://${BUCKET_NAME}

# Test downloading a file
echo "Testing file download..."
TEMP_DIR=$(mktemp -d)
FILE=$(gsutil ls gs://${BUCKET_NAME} | head -n 1)
if [ -n "${FILE}" ]; then
    gsutil cp ${FILE} ${TEMP_DIR}
    echo "Successfully downloaded ${FILE} to ${TEMP_DIR}"
    rm -rf ${TEMP_DIR}
else
    echo "No files found in the bucket."
fi

echo "Storage access test completed."
