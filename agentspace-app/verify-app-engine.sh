#!/bin/bash

# Set variables
APP_URL="https://lucid-inquiry-453823-b0.uw.r.appspot.com"

echo "Verifying App Engine deployment..."
echo "Application URL: $APP_URL"

# Test health endpoint
echo "Testing health endpoint..."
curl -s $APP_URL/api/health
echo ""

# Test languages endpoint
echo "Testing languages endpoint..."
curl -s $APP_URL/api/languages
echo ""

# Test main page
echo "Testing main page..."
curl -s -I $APP_URL

# Test static resources
echo "Testing static resources..."
curl -s -I $APP_URL/static/css/styles.css
curl -s -I $APP_URL/static/js/app.js

echo "Verification completed."
