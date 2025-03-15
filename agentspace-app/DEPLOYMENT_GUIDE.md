# Hippo Family Club Application Deployment Guide

このガイドは、Hippo Family Clubアプリケーションを Google Cloud Platform (GCP) Cloud Run にデプロイする方法を説明します。
This guide explains how to deploy the Hippo Family Club application to Google Cloud Platform (GCP) Cloud Run.

## 目次 / Table of Contents

1. [前提条件 / Prerequisites](#前提条件--prerequisites)
2. [GCPプロジェクトの設定 / GCP Project Setup](#gcpプロジェクトの設定--gcp-project-setup)
3. [サービスアカウントの作成 / Service Account Creation](#サービスアカウントの作成--service-account-creation)
4. [ローカル開発環境の設定 / Local Development Environment Setup](#ローカル開発環境の設定--local-development-environment-setup)
5. [アプリケーションのビルドとテスト / Building and Testing the Application](#アプリケーションのビルドとテスト--building-and-testing-the-application)
6. [Cloud Runへのデプロイ / Deploying to Cloud Run](#cloud-runへのデプロイ--deploying-to-cloud-run)
7. [トラブルシューティング / Troubleshooting](#トラブルシューティング--troubleshooting)

## 前提条件 / Prerequisites

- GCPアカウントとプロジェクト / GCP account and project
- Google Cloud SDKのインストール / Google Cloud SDK installed
- Dockerのインストール / Docker installed
- Gitのインストール / Git installed

## GCPプロジェクトの設定 / GCP Project Setup

### 日本語

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセスします
2. プロジェクトを選択または新規作成します
3. 以下のAPIを有効にします:
   - Cloud Run API
   - Cloud Storage API
   - Container Registry API
   - Cloud Build API

### English

1. Access the [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a new project
3. Enable the following APIs:
   - Cloud Run API
   - Cloud Storage API
   - Container Registry API
   - Cloud Build API

## サービスアカウントの作成 / Service Account Creation

### 日本語

1. Google Cloud Consoleで「IAMと管理」→「サービスアカウント」に移動します
2. 「サービスアカウントを作成」をクリックします
3. 名前を入力します（例：`hippoapp-service`）
4. 以下の役割を付与します:
   - Cloud Run サービスエージェント
   - Storage オブジェクト閲覧者
5. 「完了」をクリックします
6. サービスアカウントのリストから作成したアカウントを選択し、「鍵を作成」→「JSON」を選択します
7. ダウンロードしたJSONファイルを安全な場所に保存します

### English

1. In the Google Cloud Console, go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Enter a name (e.g., `hippoapp-service`)
4. Assign the following roles:
   - Cloud Run Service Agent
   - Storage Object Viewer
5. Click "Done"
6. From the service account list, select the account you created and click "Create Key" → "JSON"
7. Save the downloaded JSON file in a secure location

## ローカル開発環境の設定 / Local Development Environment Setup

### 日本語

1. リポジトリをクローンします:
   ```bash
   git clone https://github.com/dmasubuchi/hippoapp-gcp.git
   cd hippoapp-gcp/agentspace-app
   ```

2. サービスアカウントキーをプロジェクトに追加します:
   ```bash
   mkdir -p credentials
   # ダウンロードしたJSONキーファイルをcredentialsディレクトリにコピーし、名前を変更します
   cp /path/to/downloaded-key.json credentials/service-account-key.json
   ```

3. 環境変数を設定します:
   ```bash
   # .envファイルを編集して、GCPプロジェクトIDとバケット名を設定します
   nano .env
   ```

   `.env`ファイルの例:
   ```
   DEBUG=True
   PORT=8081
   HOST=0.0.0.0

   # GCP Configuration
   GCP_PROJECT_ID=your-project-id
   GCP_STORAGE_BUCKET=language-learning-audio
   GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json
   ```

### English

1. Clone the repository:
   ```bash
   git clone https://github.com/dmasubuchi/hippoapp-gcp.git
   cd hippoapp-gcp/agentspace-app
   ```

2. Add the service account key to the project:
   ```bash
   mkdir -p credentials
   # Copy the downloaded JSON key file to the credentials directory and rename it
   cp /path/to/downloaded-key.json credentials/service-account-key.json
   ```

3. Set up environment variables:
   ```bash
   # Edit the .env file to set your GCP project ID and bucket name
   nano .env
   ```

   Example `.env` file:
   ```
   DEBUG=True
   PORT=8081
   HOST=0.0.0.0

   # GCP Configuration
   GCP_PROJECT_ID=your-project-id
   GCP_STORAGE_BUCKET=language-learning-audio
   GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json
   ```

## アプリケーションのビルドとテスト / Building and Testing the Application

### 日本語

1. Dockerイメージをビルドします:
   ```bash
   docker build -t hippoapp:local .
   ```

2. ローカルでコンテナを実行します:
   ```bash
   docker run -d -p 8081:8080 \
     -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json \
     -v $(pwd)/credentials:/app/credentials \
     --name hippoapp-test hippoapp:local
   ```

3. ブラウザで`http://localhost:8081`にアクセスしてアプリケーションをテストします

4. テスト後、コンテナを停止します:
   ```bash
   docker stop hippoapp-test
   docker rm hippoapp-test
   ```

### English

1. Build the Docker image:
   ```bash
   docker build -t hippoapp:local .
   ```

2. Run the container locally:
   ```bash
   docker run -d -p 8081:8080 \
     -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json \
     -v $(pwd)/credentials:/app/credentials \
     --name hippoapp-test hippoapp:local
   ```

3. Access `http://localhost:8081` in your browser to test the application

4. After testing, stop the container:
   ```bash
   docker stop hippoapp-test
   docker rm hippoapp-test
   ```

## Cloud Runへのデプロイ / Deploying to Cloud Run

### 日本語

1. Google Cloud SDKで認証します:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. プロジェクトを設定します:
   ```bash
   gcloud config set project your-project-id
   ```

3. デプロイスクリプトを実行します:
   ```bash
   # スクリプトに実行権限を付与
   chmod +x deploy-to-cloud-run.sh
   
   # スクリプトを実行
   ./deploy-to-cloud-run.sh
   ```

   または、手動でデプロイします:
   ```bash
   # Dockerイメージをビルドしてコンテナレジストリにプッシュ
   docker build -t gcr.io/your-project-id/hippoapp:latest .
   docker push gcr.io/your-project-id/hippoapp:latest
   
   # Cloud Runにデプロイ
   gcloud run deploy hippoapp \
     --image gcr.io/your-project-id/hippoapp:latest \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated \
     --service-account hippoapp-service@your-project-id.iam.gserviceaccount.com \
     --set-env-vars="GCP_PROJECT_ID=your-project-id,GCP_STORAGE_BUCKET=language-learning-audio"
   ```

4. デプロイが完了すると、アプリケーションのURLが表示されます

### English

1. Authenticate with Google Cloud SDK:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. Set your project:
   ```bash
   gcloud config set project your-project-id
   ```

3. Run the deployment script:
   ```bash
   # Give execution permission to the script
   chmod +x deploy-to-cloud-run.sh
   
   # Run the script
   ./deploy-to-cloud-run.sh
   ```

   Or deploy manually:
   ```bash
   # Build and push Docker image to Container Registry
   docker build -t gcr.io/your-project-id/hippoapp:latest .
   docker push gcr.io/your-project-id/hippoapp:latest
   
   # Deploy to Cloud Run
   gcloud run deploy hippoapp \
     --image gcr.io/your-project-id/hippoapp:latest \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated \
     --service-account hippoapp-service@your-project-id.iam.gserviceaccount.com \
     --set-env-vars="GCP_PROJECT_ID=your-project-id,GCP_STORAGE_BUCKET=language-learning-audio"
   ```

4. After deployment completes, you will see the URL of your application

## トラブルシューティング / Troubleshooting

### 日本語

#### サービスアカウントの問題

- **エラー**: `Failed to load service account credentials`
- **解決策**: サービスアカウントキーが正しい形式であることを確認し、パスが正しく設定されていることを確認します

#### デプロイの問題

- **エラー**: `Container failed to start`
- **解決策**: Cloud Runのログを確認し、環境変数が正しく設定されていることを確認します

#### アプリケーションが表示されない

- **エラー**: デプロイURLにアクセスしても何も表示されない
- **解決策**: 
  1. Cloud Runのログを確認します
  2. アプリケーションが正しくビルドされていることを確認します
  3. デバッグモードを有効にして、ローカルでテストします

### English

#### Service Account Issues

- **Error**: `Failed to load service account credentials`
- **Solution**: Verify that the service account key is in the correct format and that the path is correctly set

#### Deployment Issues

- **Error**: `Container failed to start`
- **Solution**: Check the Cloud Run logs and verify that environment variables are correctly set

#### Application Not Displaying

- **Error**: Nothing displays when accessing the deployment URL
- **Solution**: 
  1. Check the Cloud Run logs
  2. Verify that the application is built correctly
  3. Enable debug mode and test locally

## アプリケーション構成図 / Application Architecture Diagram

```
+------------------+     +-------------------+     +------------------+
| User's Browser   |---->| Cloud Run Service |---->| Cloud Storage    |
| (Web Interface)  |<----| (Hippo App)       |<----| (Audio Files)    |
+------------------+     +-------------------+     +------------------+
                                  |
                                  v
                         +-------------------+
                         | Service Account   |
                         | (Authentication)  |
                         +-------------------+
```

このアーキテクチャでは:
- ユーザーはブラウザからアプリケーションにアクセスします
- アプリケーションはCloud Runでホストされています
- オーディオファイルはCloud Storageに保存されています
- サービスアカウントはCloud StorageへのアクセスをCloud Runサービスに提供します

In this architecture:
- Users access the application from their browser
- The application is hosted on Cloud Run
- Audio files are stored in Cloud Storage
- The service account provides Cloud Run service access to Cloud Storage
