# App Engine Deployment Guide

This guide provides instructions for deploying the Hippo Family Club multilingual audio player to Google App Engine.

## Prerequisites

- Google Cloud SDK installed and configured
- Access to the GCP project `lucid-inquiry-453823-b0`
- Service account with appropriate permissions

## Deployment Steps

### 1. Prepare the Application

Ensure the service account key is available:

```bash
mkdir -p credentials
cp credentials/service-account-key-template.json credentials/service-account-key.json
# Edit the file to include the actual credentials
```

### 2. Deploy to App Engine

Use the provided deployment script:

```bash
./deploy-to-app-engine.sh
```

Alternatively, deploy manually:

```bash
gcloud app deploy app.yaml --project=lucid-inquiry-453823-b0
```

### 3. Verify Deployment

After deployment, the application will be available at:

```
https://lucid-inquiry-453823-b0.uw.r.appspot.com
```

Test the following endpoints:

- Main page: `https://lucid-inquiry-453823-b0.uw.r.appspot.com/`
- Health check: `https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/health`
- Languages API: `https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/languages`

## Troubleshooting

### Service Account Issues

If you encounter authentication issues, verify that:

1. The service account has the necessary permissions (Storage Object Viewer)
2. The service account key is correctly formatted
3. The `GOOGLE_APPLICATION_CREDENTIALS` environment variable is correctly set

### Static Files Not Loading

If static files (CSS, JavaScript) are not loading:

1. Verify the `handlers` section in `app.yaml` is correctly configured
2. Check that static files are in the correct directory (`app/static`)

### Cold Start Issues

App Engine may have cold start issues for infrequently accessed applications. To mitigate this:

1. Configure minimum instances in `app.yaml`:
   ```yaml
   automatic_scaling:
     min_instances: 1
   ```

2. Use a warmup request handler:
   ```yaml
   inbound_services:
   - warmup
   ```

## Comparison with Cloud Run

App Engine is recommended for this application because:

1. It provides public access by default without requiring explicit IAM policy changes
2. It is not affected by the organization policy restrictions that affect Cloud Run
3. It has a simpler deployment process
4. The application is already configured for App Engine

For more details on the differences between Cloud Run and App Engine, see the [Cloud Run vs App Engine Comparison](CLOUD_RUN_VS_APP_ENGINE.md) document.

## Japanese Guide / 日本語ガイド

### 前提条件

- Google Cloud SDKがインストールされ、設定されていること
- GCPプロジェクト `lucid-inquiry-453823-b0` へのアクセス権
- 適切な権限を持つサービスアカウント

### デプロイ手順

#### 1. アプリケーションの準備

サービスアカウントキーが利用可能であることを確認します：

```bash
mkdir -p credentials
cp credentials/service-account-key-template.json credentials/service-account-key.json
# 実際の認証情報を含むようにファイルを編集します
```

#### 2. App Engineへのデプロイ

提供されているデプロイスクリプトを使用します：

```bash
./deploy-to-app-engine.sh
```

または、手動でデプロイします：

```bash
gcloud app deploy app.yaml --project=lucid-inquiry-453823-b0
```

#### 3. デプロイの確認

デプロイ後、アプリケーションは以下のURLで利用可能になります：

```
https://lucid-inquiry-453823-b0.uw.r.appspot.com
```

以下のエンドポイントをテストします：

- メインページ: `https://lucid-inquiry-453823-b0.uw.r.appspot.com/`
- ヘルスチェック: `https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/health`
- 言語API: `https://lucid-inquiry-453823-b0.uw.r.appspot.com/api/languages`
