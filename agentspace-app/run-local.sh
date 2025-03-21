#!/bin/bash
# Run the Hippo Family Club application locally

set -e

# Set environment variables
export GCP_PROJECT_ID=lucid-inquiry-453823-b0
export GCP_STORAGE_BUCKET=language-learning-audio
export DEBUG=True
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/credentials/service-account-key.json

# Run the application
echo "Starting the application locally..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
