# App Engine Deployment Verification

This document provides instructions for verifying the App Engine deployment of the Hippo Family Club multilingual audio player.

## Verification Steps

### 1. Check Deployment Status

After deploying to App Engine, verify the deployment status:

```bash
gcloud app describe --project=lucid-inquiry-453823-b0
```

### 2. Test Public Access

Verify that the application is publicly accessible:

```bash
curl -s https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/health
```

Expected response:
```json
{"status": "healthy"}
```

### 3. Test API Endpoints

Test the languages API endpoint:

```bash
curl -s https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/languages
```

Expected response:
```json
{
  "en": {
    "name": "English",
    "display_name": "English",
    "flag": "🇺🇸",
    "direction": "ltr"
  },
  "ja": {
    "name": "Japanese",
    "display_name": "日本語",
    "flag": "🇯🇵",
    "direction": "ltr"
  },
  ...
}
```

### 4. Test Static Files

Verify that static files are being served correctly:

```bash
curl -I https://lucid-inquiry-453823-b0.uw.r.appspot.com/static/css/styles.css
curl -I https://lucid-inquiry-453823-b0.uw.r.appspot.com/static/js/app.js
```

Expected response:
```
HTTP/2 200
...
```

### 5. Test Audio Playback

Test the audio playback API:

```bash
curl -I https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/audio/play?file_id=test.mp3
```

## Troubleshooting

### 404 Errors

If you encounter 404 errors:

1. Verify that the App Engine application is deployed:
   ```bash
   gcloud app versions list --project=lucid-inquiry-453823-b0
   ```

2. Check the App Engine logs:
   ```bash
   gcloud app logs tail --project=lucid-inquiry-453823-b0
   ```

### 403 Errors

If you encounter 403 errors:

1. Verify that the service account has the necessary permissions:
   ```bash
   gcloud projects get-iam-policy lucid-inquiry-453823-b0 --format=json | grep hippoapp-service
   ```

2. Check that the service account key is correctly configured in the app.yaml file.

## Japanese Guide / 日本語ガイド

### 検証手順

#### 1. デプロイ状態の確認

App Engineへのデプロイ後、デプロイ状態を確認します：

```bash
gcloud app describe --project=lucid-inquiry-453823-b0
```

#### 2. パブリックアクセスのテスト

アプリケーションが公開アクセス可能であることを確認します：

```bash
curl -s https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/health
```

期待される応答：
```json
{"status": "healthy"}
```

#### 3. APIエンドポイントのテスト

言語APIエンドポイントをテストします：

```bash
curl -s https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/languages
```

#### 4. 静的ファイルのテスト

静的ファイルが正しく提供されていることを確認します：

```bash
curl -I https://lucid-inquiry-453823-b0.uw.r.appspot.com/static/css/styles.css
curl -I https://lucid-inquiry-453823-b0.uw.r.appspot.com/static/js/app.js
```

#### 5. オーディオ再生のテスト

オーディオ再生APIをテストします：

```bash
curl -I https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/audio/play?file_id=test.mp3
```
