# Organization Policy Guide for Cloud Run

## Overview

This guide explains how to modify the organization policy to allow unauthenticated access to Cloud Run services.

## Current Status

The Cloud Run service is deployed but requires authentication due to organization policy restrictions. The error message indicates:

```
Contact your GCP administrator to:
Modify the organization policy to allow unauthenticated access to Cloud Run services
Or set up Identity-Aware Proxy (IAP) for authenticated access
```

## Required Changes

To allow unauthenticated access to Cloud Run services, the organization policy needs to be modified. This requires administrative privileges.

### Option 1: Modify Organization Policy via Google Cloud Console (Recommended)

1. Go to the Google Cloud Console
2. Navigate to IAM & Admin > Organization Policies
3. Search for "Domain restricted sharing" or "iam.allowedPolicyMemberDomains"
4. Edit the policy to allow `allUsers` for Cloud Run services
5. Apply the changes

### Option 2: Use the gcloud Command (Requires Admin Access)

```bash
# Apply the organization policy
gcloud org-policies set-policy cloud-run-policy.yaml
```

### Option 3: Update Cloud Run Service IAM Policy Directly

If the organization policy has already been modified to allow public access, you can update the Cloud Run service IAM policy directly:

```bash
# Update the Cloud Run service IAM policy
gcloud run services set-iam-policy hippoapp --region=us-west1 policy.yaml
```

### Option 4: Set Up Identity-Aware Proxy (IAP)

If modifying the organization policy is not possible, you can set up IAP to provide authenticated access to the Cloud Run service.

## Workaround for Testing

For testing purposes, you can run the application locally using:

```bash
./run-local.sh
```

This will start the application with mock data and allow you to test the functionality without requiring organization policy changes.
