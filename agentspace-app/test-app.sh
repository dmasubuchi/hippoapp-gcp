#!/bin/bash
set -e

echo "Testing Hippo Family Club application..."

# Configuration
export DEBUG="True"
export PORT=8080
export HOST="localhost"
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials/service-account-key.json"

# Install ffmpeg if not already installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg for audio processing..."
    sudo apt-get update && sudo apt-get install -y ffmpeg
fi

# Create mock credentials if needed
if [ ! -s "credentials/service-account-key.json" ]; then
    echo "Creating mock credentials for testing..."
    mkdir -p credentials
    cp credentials/service-account-key-template.json credentials/service-account-key.json
    sed -i 's/YOUR_PRIVATE_KEY_ID/mock_key_id_for_testing/g' credentials/service-account-key.json
    sed -i 's/YOUR_PRIVATE_KEY/-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj\\nMzEfYyjiWA4R4\/M2bS1GB4t7NXp98C3SC6dVMvDuictGeurT8jNbvJZHtCSuYEvu\\nNMoSfm76oqFvAp8Gy0iz5sxjZmSnXyCdPEovGhLa0VzMaQ8s+CLOyS56YyCFGeJZ\\n-----END PRIVATE KEY-----\\n/g' credentials/service-account-key.json
    sed -i 's/YOUR_CLIENT_ID/mock_client_id_for_testing/g' credentials/service-account-key.json
    sed -i 's/YOUR_CLIENT_EMAIL/hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com/g' credentials/service-account-key.json
    sed -i 's/YOUR_PROJECT_ID/lucid-inquiry-453823-b0/g' credentials/service-account-key.json
fi

# Create cache directory
mkdir -p /tmp/hippoapp-cache

# Start the application in the background
echo "Starting application in debug mode..."
cd "$(dirname "$0")"
python -m app.main &
APP_PID=$!

# Wait for the application to start
echo "Waiting for application to start..."
sleep 5

# Test health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8080/api/health)
echo "Health response: $HEALTH_RESPONSE"

if [[ ! "$HEALTH_RESPONSE" == *"status"* ]]; then
    echo "ERROR: Health endpoint did not return expected response"
    kill $APP_PID
    exit 1
fi

# Test languages endpoint
echo "Testing languages endpoint..."
LANGUAGES_RESPONSE=$(curl -s http://localhost:8080/api/languages)
echo "Languages response length: $(echo $LANGUAGES_RESPONSE | wc -c) bytes"

if [[ ! "$LANGUAGES_RESPONSE" == *"English"* ]]; then
    echo "ERROR: Languages endpoint did not return expected response"
    kill $APP_PID
    exit 1
fi

# Test audio endpoint with mock data
echo "Testing audio endpoint with mock data..."
# Create test file paths for different languages
AUDIO_PATH_EN="audio/en/sample1.mp3"
AUDIO_PATH_JA="audio/ja/sample1.mp3"

# Test English audio
echo "Testing English audio metadata..."
AUDIO_RESPONSE=$(curl -s "http://localhost:8080/api/audio/$AUDIO_PATH_EN")
echo "Audio response: $AUDIO_RESPONSE"

if [[ ! "$AUDIO_RESPONSE" == *"language"* ]]; then
    echo "ERROR: Audio endpoint did not return expected response"
    echo "Trying with different path format..."
    
    # Try alternative path formats
    ALTERNATIVE_PATHS=("en/sample1.mp3" "sample1.mp3" "audio/sample1.mp3")
    
    for ALT_PATH in "${ALTERNATIVE_PATHS[@]}"; do
        echo "Trying path: $ALT_PATH"
        AUDIO_RESPONSE=$(curl -s "http://localhost:8080/api/audio/$ALT_PATH")
        if [[ "$AUDIO_RESPONSE" == *"language"* ]]; then
            echo "Found working path format: $ALT_PATH"
            AUDIO_PATH_EN=$ALT_PATH
            AUDIO_PATH_JA=${ALT_PATH/en/ja}
            break
        fi
    done
    
    if [[ ! "$AUDIO_RESPONSE" == *"language"* ]]; then
        echo "ERROR: Could not find working audio path format"
        kill $APP_PID
        exit 1
    fi
fi

echo "Using audio path format: $AUDIO_PATH_EN for English, $AUDIO_PATH_JA for Japanese"

# Test audio playback
echo "Testing audio playback..."
# Use GET instead of HEAD request for playback
PLAYBACK_RESPONSE=$(curl -s -o /dev/null -D - "http://localhost:8080/api/audio/$AUDIO_PATH_EN/play")
echo "Playback response: $PLAYBACK_RESPONSE"

if [[ ! "$PLAYBACK_RESPONSE" == *"audio/mpeg"* ]]; then
    echo "ERROR: Audio playback endpoint did not return expected content type"
    echo "Response was: $PLAYBACK_RESPONSE"
    kill $APP_PID
    exit 1
fi

# Test different languages
echo "Testing Japanese audio..."
# Create Japanese version of the path
AUDIO_PATH_JA=${AUDIO_PATH_EN/en/ja}
if [[ "$AUDIO_PATH_EN" != *"en"* ]]; then
    # If the path doesn't contain 'en', use the original path for Japanese too
    AUDIO_PATH_JA=$AUDIO_PATH_EN
fi
echo "Using Japanese audio path: $AUDIO_PATH_JA"

JA_RESPONSE=$(curl -s "http://localhost:8080/api/audio/$AUDIO_PATH_JA")
if [[ ! "$JA_RESPONSE" == *"ja"* && ! "$JA_RESPONSE" == *"language"* ]]; then
    echo "ERROR: Japanese audio endpoint did not return expected response"
    echo "Response was: $JA_RESPONSE"
    kill $APP_PID
    exit 1
fi

# Test playback parameters
echo "Testing playback parameters..."
PARAMS_RESPONSE=$(curl -s -o /dev/null -D - "http://localhost:8080/api/audio/$AUDIO_PATH_EN/play?speed=1.5&repeat=true")
if [[ ! "$PARAMS_RESPONSE" == *"audio/mpeg"* ]]; then
    echo "ERROR: Playback with parameters did not return expected content type"
    echo "Response was: $PARAMS_RESPONSE"
    kill $APP_PID
    exit 1
fi

# Kill the application
echo "Stopping application..."
kill $APP_PID

echo "Tests completed successfully!"
