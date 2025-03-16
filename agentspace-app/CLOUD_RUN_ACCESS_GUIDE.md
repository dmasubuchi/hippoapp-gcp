# Cloud Run Public Access Guide

This guide provides instructions for enabling public access to the Cloud Run service.

## Option 1: Using Google Cloud Console (Recommended)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to Cloud Run
3. Select the "hippoapp" service
4. Click on "PERMISSIONS" tab
5. Click "ADD PRINCIPAL"
6. In the "New principals" field, enter "allUsers"
7. For the role, select "Cloud Run Invoker"
8. Click "SAVE"

## Option 2: Using gcloud Command Line

Run the following command:

```bash
gcloud run services add-iam-policy-binding hippoapp \
  --region=us-west1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

## Option 3: Using the Provided Script

Run the provided script:

```bash
./apply-cloud-run-policy.sh
```

## Verification

After applying the policy, verify that the service is accessible by visiting:
https://hippoapp-546tyu2ata-uw.a.run.app

You should be able to access the application without authentication.
