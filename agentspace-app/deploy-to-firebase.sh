#!/bin/bash
set -e

# Configuration
export PROJECT_ID=lucid-inquiry-453823-b0

echo "Starting Firebase deployment..."

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Login to Firebase
firebase login --no-localhost

# Initialize Firebase project
firebase use --add $PROJECT_ID

# Deploy to Firebase Hosting
firebase deploy --only hosting

echo "Deployment completed!"
echo "Application URL: https://$PROJECT_ID.web.app"
