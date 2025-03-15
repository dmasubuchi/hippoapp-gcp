# Hippo Family Club Application - GCP Cloud Run Deployment Guide

## Introduction

This guide explains how to deploy the Hippo Family Club multilingual audio player application to Google Cloud Run in a beginner-friendly way.

## Prerequisites

- Google Cloud account
- Google Cloud SDK (installation instructions below)
- Docker (installation instructions below)

## 1. Installing Google Cloud SDK

### For Windows
1. Download the [Google Cloud SDK installer](https://cloud.google.com/sdk/docs/install)
2. Run the downloaded installer and follow the on-screen instructions
3. After installation, open Command Prompt and run `gcloud init`

### For Mac
1. Open Terminal
2. Run the following commands:
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

### For Linux
1. Open Terminal
2. Run the following commands:
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

## 2. Installing Docker

### For Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the on-screen instructions

### For Mac
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the on-screen instructions

### For Linux
1. Open Terminal
2. Run the following commands:
   ```bash
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

## 3. Google Cloud Authentication

1. Open Terminal or Command Prompt
2. Run the following command:
   ```bash
   gcloud auth login
   ```
3. A browser will open asking you to log in with your Google account
4. After logging in, set the project with:
   ```bash
   gcloud config set project lucid-inquiry-453823-b0
   ```

## 4. Service Account Setup

### Creating a Service Account Key
1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. From the left menu, select "IAM & Admin" → "Service Accounts"
3. Select "hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com"
4. Select the "Keys" tab, then click "Add Key" → "Create new key"
5. Select "JSON" as the key type and click "Create"
6. The key file will be automatically downloaded

### Securely Storing the Key File
1. Save the downloaded key file in a secure location
2. Do not commit this file to the repository as it contains sensitive information
3. Set the environment variable:
   ```bash
   # For Windows
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key-file.json
   
   # For Mac/Linux
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key-file.json
   ```

## 5. Building and Deploying the Application

### Building the Docker Image
1. Navigate to the repository root directory:
   ```bash
   cd /path/to/hippoapp-gcp/agentspace-app
   ```
2. Build the Docker image:
   ```bash
   docker build -t gcr.io/lucid-inquiry-453823-b0/hippoapp:latest .
   ```

### Pushing the Image
1. Authenticate to Google Container Registry:
   ```bash
   gcloud auth configure-docker
   ```
2. Push the image:
   ```bash
   docker push gcr.io/lucid-inquiry-453823-b0/hippoapp:latest
   ```

### Deploying to Cloud Run
1. Deploy with the following command:
   ```bash
   gcloud run deploy hippoapp \
     --image gcr.io/lucid-inquiry-453823-b0/hippoapp:latest \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated \
     --service-account hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com \
     --set-env-vars="GCP_PROJECT_ID=lucid-inquiry-453823-b0,GCP_STORAGE_BUCKET=language-learning-audio"
   ```
2. When deployment completes, you'll receive a URL for your application

## 6. Using Secret Manager (Recommended)

For secure credential management, we recommend using Google Cloud Secret Manager:

1. Create a secret:
   ```bash
   gcloud secrets create hippoapp-sa-key --data-file=/path/to/service-account-key.json
   ```

2. Grant access to the service account:
   ```bash
   gcloud secrets add-iam-policy-binding hippoapp-sa-key \
     --member=serviceAccount:hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com \
     --role=roles/secretmanager.secretAccessor
   ```

3. Update the Cloud Run service:
   ```bash
   gcloud run services update hippoapp \
     --region=us-west1 \
     --update-secrets=GOOGLE_APPLICATION_CREDENTIALS=hippoapp-sa-key:latest
   ```

## 7. Verifying the Application

1. Access the URL provided after deployment
2. Verify the following features work correctly:
   - Audio file playback
   - Language switching (using left/right arrow buttons)
   - Sentence highlighting

## Troubleshooting

### If You Can't Access the Application
- Verify that the Cloud Run service deployed successfully
- Check that the service allows unauthenticated access

### If Audio Files Don't Play
- Verify that the service account has the correct permissions
- Check access to the GCS bucket "language-learning-audio"

### How to Check Error Logs
1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. From the left menu, select "Cloud Run"
3. Click on the "hippoapp" service
4. Select the "Logs" tab to view errors

## Security Best Practices

1. Never commit service account keys to the repository
2. Follow the principle of least privilege by granting only necessary permissions
3. Use Secret Manager to manage sensitive information
4. Rotate service account keys regularly

## Summary

This guide has walked you through deploying the Hippo Family Club multilingual audio player application to Google Cloud Run. If you have any questions or issues, please contact the development team.
