# Cloud Run Public Access Guide

## Step 1: Access Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Make sure you're logged in with an account that has administrative privileges
3. Select the project: `lucid-inquiry-453823-b0`

## Step 2: Modify Organization Policy

1. Navigate to IAM & Admin > Organization Policies
2. Search for "Domain restricted sharing" or "iam.allowedPolicyMemberDomains"
3. Click on the policy to edit it
4. Click "Edit" at the top of the page
5. Under "Policy enforcement", select "Customize"
6. Add a new rule:
   - Condition: `resource.service == "run.googleapis.com"`
   - Policy values: Allow `allUsers` and `allAuthenticatedUsers`
7. Click "Save"

## Step 3: Update Cloud Run Service IAM Policy

1. Navigate to Cloud Run in the Google Cloud Console
2. Select the `hippoapp` service
3. Go to the "Permissions" tab
4. Click "Add Principal"
5. In the "New principals" field, enter `allUsers`
6. For the role, select "Cloud Run Invoker"
7. Click "Save"

## Step 4: Verify Public Access

1. Access the service URL: `https://hippoapp-546tyu2ata-uw.a.run.app`
2. Verify that you can access the application without authentication
3. Test the API endpoints:
   - `/api/health`
   - `/api/languages`

## Alternative: Command Line Approach

If you prefer using the command line, you can use the provided scripts:

```bash
# Apply the organization policy and update the Cloud Run service IAM policy
./apply-organization-policy.sh
```

## Troubleshooting

If you encounter permission issues, make sure:
1. You have the necessary administrative privileges
2. The organization policy allows public access to Cloud Run services
3. The Cloud Run service IAM policy allows `allUsers` with the `roles/run.invoker` role
