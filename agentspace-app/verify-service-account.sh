#!/bin/bash
set -e

echo "Verifying service account key..."
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

echo "Service account key is valid."
exit 0
