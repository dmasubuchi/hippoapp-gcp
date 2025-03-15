# Hippo Family Club アプリケーション - GCP Cloud Run デプロイガイド

## はじめに

このガイドでは、Hippo Family Club の多言語オーディオプレーヤーアプリケーションを Google Cloud Run にデプロイする方法を初心者向けに説明します。

## 前提条件

- Google Cloud アカウント
- Google Cloud SDK（インストール方法は後述）
- Docker（インストール方法は後述）

## 1. Google Cloud SDK のインストール

### Windows の場合
1. [Google Cloud SDK インストーラー](https://cloud.google.com/sdk/docs/install) をダウンロード
2. ダウンロードしたインストーラーを実行し、画面の指示に従ってインストール
3. インストール完了後、コマンドプロンプトを開き `gcloud init` を実行

### Mac の場合
1. ターミナルを開く
2. 以下のコマンドを実行:
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

### Linux の場合
1. ターミナルを開く
2. 以下のコマンドを実行:
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

## 2. Docker のインストール

### Windows の場合
1. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) をダウンロード
2. インストーラーを実行し、画面の指示に従ってインストール

### Mac の場合
1. [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop) をダウンロード
2. インストーラーを実行し、画面の指示に従ってインストール

### Linux の場合
1. ターミナルを開く
2. 以下のコマンドを実行:
   ```bash
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

## 3. Google Cloud の認証

1. ターミナルまたはコマンドプロンプトを開く
2. 以下のコマンドを実行:
   ```bash
   gcloud auth login
   ```
3. ブラウザが開き、Google アカウントでログインするよう求められます
4. ログイン後、以下のコマンドでプロジェクトを設定:
   ```bash
   gcloud config set project lucid-inquiry-453823-b0
   ```

## 4. サービスアカウントの設定

### サービスアカウントキーの作成
1. [Google Cloud Console](https://console.cloud.google.com) にアクセス
2. 左側のメニューから「IAM と管理」→「サービスアカウント」を選択
3. 「hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com」を選択
4. 「キー」タブを選択し、「鍵を追加」→「新しい鍵を作成」をクリック
5. キーのタイプとして「JSON」を選択し、「作成」をクリック
6. キーファイルが自動的にダウンロードされます

### キーファイルの安全な保管
1. ダウンロードしたキーファイルを安全な場所に保存
2. このファイルは秘密情報なので、リポジトリにコミットしないでください
3. 環境変数を設定:
   ```bash
   # Windows の場合
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key-file.json
   
   # Mac/Linux の場合
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key-file.json
   ```

## 5. アプリケーションのビルドとデプロイ

### Docker イメージのビルド
1. リポジトリのルートディレクトリに移動:
   ```bash
   cd /path/to/hippoapp-gcp/agentspace-app
   ```
2. Docker イメージをビルド:
   ```bash
   docker build -t gcr.io/lucid-inquiry-453823-b0/hippoapp:latest .
   ```

### イメージのプッシュ
1. Google Container Registry に認証:
   ```bash
   gcloud auth configure-docker
   ```
2. イメージをプッシュ:
   ```bash
   docker push gcr.io/lucid-inquiry-453823-b0/hippoapp:latest
   ```

### Cloud Run へのデプロイ
1. 以下のコマンドでデプロイ:
   ```bash
   gcloud run deploy hippoapp \
     --image gcr.io/lucid-inquiry-453823-b0/hippoapp:latest \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated \
     --service-account hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com \
     --set-env-vars="GCP_PROJECT_ID=lucid-inquiry-453823-b0,GCP_STORAGE_BUCKET=language-learning-audio"
   ```
2. デプロイが完了すると、アプリケーションの URL が表示されます

## 6. シークレットマネージャーの使用（推奨）

サービスアカウントキーを安全に管理するために、Google Cloud のシークレットマネージャーを使用することをお勧めします。

1. シークレットの作成:
   ```bash
   gcloud secrets create hippoapp-sa-key --data-file=/path/to/service-account-key.json
   ```

2. サービスアカウントにアクセス権を付与:
   ```bash
   gcloud secrets add-iam-policy-binding hippoapp-sa-key \
     --member=serviceAccount:hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com \
     --role=roles/secretmanager.secretAccessor
   ```

3. Cloud Run サービスの更新:
   ```bash
   gcloud run services update hippoapp \
     --region=us-west1 \
     --update-secrets=GOOGLE_APPLICATION_CREDENTIALS=hippoapp-sa-key:latest
   ```

## 7. アプリケーションの確認

1. デプロイ時に表示された URL にアクセス
2. 以下の機能が正常に動作することを確認:
   - オーディオファイルの再生
   - 言語切り替え（左右の矢印ボタン）
   - センテンスのハイライト表示

## トラブルシューティング

### アプリケーションにアクセスできない場合
- Cloud Run サービスが正常にデプロイされたか確認
- サービスが「未認証」アクセスを許可しているか確認

### オーディオファイルが再生されない場合
- サービスアカウントに適切な権限があるか確認
- GCS バケット「language-learning-audio」にアクセスできるか確認

### エラーログの確認方法
1. [Google Cloud Console](https://console.cloud.google.com) にアクセス
2. 左側のメニューから「Cloud Run」を選択
3. サービス「hippoapp」をクリック
4. 「ログ」タブを選択してエラーを確認

## セキュリティのベストプラクティス

1. サービスアカウントキーをリポジトリにコミットしない
2. 最小権限の原則に従い、必要な権限のみを付与
3. シークレットマネージャーを使用して機密情報を管理
4. 定期的にサービスアカウントキーをローテーション

## まとめ

このガイドでは、Hippo Family Club の多言語オーディオプレーヤーアプリケーションを Google Cloud Run にデプロイする方法を説明しました。質問や問題がある場合は、開発チームにお問い合わせください。
