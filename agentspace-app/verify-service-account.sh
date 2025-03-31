#!/bin/bash
set -e

echo "Verifying service account key..."

# Check if file exists and is not empty
if [ ! -s "credentials/service-account-key.json" ]; then
    echo "ERROR: Service account key is empty or does not exist."
    exit 1
fi

# Check if the file is valid JSON
if ! jq . credentials/service-account-key.json > /dev/null 2>&1; then
    echo "ERROR: Service account key is not valid JSON."
    exit 1
fi

# Check if the file has the required fields
if ! jq -e '.private_key and .client_email and .project_id' credentials/service-account-key.json > /dev/null 2>&1; then
    echo "ERROR: Service account key is missing required fields."
    exit 1
fi

# Check if the project ID matches the expected project
PROJECT_ID=$(jq -r '.project_id' credentials/service-account-key.json)
EXPECTED_PROJECT_ID="lucid-inquiry-453823-b0"

if [ "$PROJECT_ID" != "$EXPECTED_PROJECT_ID" ]; then
    echo "WARNING: Service account project ID ($PROJECT_ID) does not match expected project ID ($EXPECTED_PROJECT_ID)."
    # Continue but warn the user
fi

# Check if the service account email has the correct format
CLIENT_EMAIL=$(jq -r '.client_email' credentials/service-account-key.json)
if [[ ! "$CLIENT_EMAIL" =~ .*@.*\.iam\.gserviceaccount\.com$ ]]; then
    echo "WARNING: Service account email ($CLIENT_EMAIL) does not have the expected format."
    # Continue but warn the user
fi

echo "Service account key is valid."
exit 0
