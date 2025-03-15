# Google Cloud Setup Guide for Hippo Family Club Application

This guide provides step-by-step instructions for setting up Google Cloud Platform (GCP) services required for the Hippo Family Club language learning application.

## Prerequisites

- Google account (matthew@almeisan.net)
- Google Cloud project (lucid-inquiry-453823-b0)
- Billing account configured

## 1. Enable Required APIs

The application requires the following Google Cloud APIs:

1. **Cloud Speech-to-Text API**
   - Navigate to: https://console.cloud.google.com/apis/library/speech.googleapis.com
   - Click "Enable"

2. **Cloud Translation API**
   - Navigate to: https://console.cloud.google.com/apis/library/translate.googleapis.com
   - Click "Enable"

3. **Cloud Storage**
   - Navigate to: https://console.cloud.google.com/apis/library/storage-component.googleapis.com
   - Click "Enable"

4. **Firestore**
   - Navigate to: https://console.cloud.google.com/apis/library/firestore.googleapis.com
   - Click "Enable"

## 2. Create a Service Account

1. Navigate to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "Create Service Account"
3. Enter the following details:
   - Service account name: `hippoapp-service`
   - Service account ID: `hippoapp-service`
   - Description: `Service account for Hippo Family Club application`
4. Click "Create and Continue"
5. Add the following roles:
   - Storage Admin (`roles/storage.admin`)
   - Speech-to-Text Admin (`roles/speech.admin`)
   - Cloud Translation API User (`roles/cloudtranslate.user`)
   - Firestore User (`roles/datastore.user`)
6. Click "Continue" and then "Done"

## 3. Create and Download Service Account Key

1. From the Service Accounts page, click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON" as the key type
5. Click "Create"
6. Save the downloaded JSON key file to a secure location

## 4. Set Up Cloud Storage Bucket

1. Navigate to: https://console.cloud.google.com/storage/browser
2. Click "Create Bucket"
3. Enter a unique name for your bucket (e.g., `hippoapp-audio-storage`)
4. Choose a location type (Region recommended)
5. Select a region close to your users (e.g., `asia-northeast1` for Japan)
6. Leave default settings for storage class (Standard)
7. Leave default settings for access control (Fine-grained)
8. Click "Create"

## 5. Configure Firestore Database

1. Navigate to: https://console.cloud.google.com/firestore
2. Click "Create Database"
3. Select "Native mode"
4. Choose a location close to your users
5. Click "Create"

## 6. Set Environment Variables

### Linux/Mac

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
```

### Windows (PowerShell)

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your-service-account-key.json"
```

## 7. Test Authentication

1. Navigate to your project directory
2. Run the authentication test:

```bash
python demo.py --auth
```

If successful, you should see confirmation that all required services are accessible.

## 8. Upload Sample Audio Files

1. Navigate to your Cloud Storage bucket in the console
2. Click "Upload Files"
3. Select audio files for testing
4. Click "Open"

## 9. Test Transcription

```bash
python -m data-ingestion.scripts.transcribe --gcs-uri gs://your-bucket-name/your-audio-file.mp3 --output results.json
```

## 10. Test Web Application

```bash
python demo.py --web
```

## Troubleshooting

### Authentication Issues

- Verify that the GOOGLE_APPLICATION_CREDENTIALS environment variable is set correctly
- Ensure the service account has the necessary permissions
- Check that all required APIs are enabled

### API Quota Limits

- If you encounter quota limits, you may need to request quota increases in the Google Cloud Console

### Storage Access Issues

- Verify bucket permissions
- Check that the service account has Storage Admin role

## Additional Resources

- [Google Cloud Speech-to-Text Documentation](https://cloud.google.com/speech-to-text/docs)
- [Google Cloud Translation Documentation](https://cloud.google.com/translate/docs)
- [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Firestore Documentation](https://cloud.google.com/firestore/docs)
