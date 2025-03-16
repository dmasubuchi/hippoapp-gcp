#!/bin/bash
set -e

# Configuration
export APP_URL="https://lucid-inquiry-453823-b0.uw.r.appspot.com"

# Check if the application is accessible
echo "Checking if the application is accessible..."
if curl -s -f -o /dev/null "$APP_URL"; then
    echo "✅ Application is accessible at $APP_URL"
else
    echo "❌ Application is not accessible at $APP_URL"
    exit 1
fi

# Check health endpoint
echo "Checking health endpoint..."
HEALTH_RESPONSE=$(curl -s "$APP_URL/api/health")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ Health check passed: $HEALTH_RESPONSE"
else
    echo "❌ Health check failed: $HEALTH_RESPONSE"
    exit 1
fi

# Check languages endpoint
echo "Checking languages endpoint..."
LANGUAGES_RESPONSE=$(curl -s "$APP_URL/api/languages")
if echo "$LANGUAGES_RESPONSE" | grep -q "en"; then
    echo "✅ Languages endpoint working: $LANGUAGES_RESPONSE"
else
    echo "❌ Languages endpoint failed: $LANGUAGES_RESPONSE"
    exit 1
fi

# Check audio endpoint
echo "Checking audio endpoint..."
AUDIO_RESPONSE=$(curl -s "$APP_URL/api/audio/sample1")
if echo "$AUDIO_RESPONSE" | grep -q "name"; then
    echo "✅ Audio endpoint working: $AUDIO_RESPONSE"
else
    echo "❌ Audio endpoint failed: $AUDIO_RESPONSE"
    exit 1
fi

echo "All verification checks passed! The application is deployed and working correctly."
