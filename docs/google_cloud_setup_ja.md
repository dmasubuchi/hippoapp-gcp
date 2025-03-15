# ヒッポファミリークラブアプリケーションのためのGoogle Cloud設定ガイド

このガイドでは、ヒッポファミリークラブ言語学習アプリケーションに必要なGoogle Cloud Platform (GCP)サービスの設定手順を説明します。

## 前提条件

- Googleアカウント (matthew@almeisan.net)
- Google Cloudプロジェクト (lucid-inquiry-453823-b0)
- 請求先アカウントの設定完了

## 1. 必要なAPIの有効化

アプリケーションには以下のGoogle Cloud APIが必要です：

1. **Cloud Speech-to-Text API**
   - 以下のURLにアクセス: https://console.cloud.google.com/apis/library/speech.googleapis.com
   - 「有効にする」をクリック

2. **Cloud Translation API**
   - 以下のURLにアクセス: https://console.cloud.google.com/apis/library/translate.googleapis.com
   - 「有効にする」をクリック

3. **Cloud Storage**
   - 以下のURLにアクセス: https://console.cloud.google.com/apis/library/storage-component.googleapis.com
   - 「有効にする」をクリック

4. **Firestore**
   - 以下のURLにアクセス: https://console.cloud.google.com/apis/library/firestore.googleapis.com
   - 「有効にする」をクリック

## 2. サービスアカウントの作成

1. 以下のURLにアクセス: https://console.cloud.google.com/iam-admin/serviceaccounts
2. 「サービスアカウントを作成」をクリック
3. 以下の詳細を入力:
   - サービスアカウント名: `hippoapp-service`
   - サービスアカウントID: `hippoapp-service`
   - 説明: `ヒッポファミリークラブアプリケーション用サービスアカウント`
4. 「作成して続行」をクリック
5. 以下の役割を追加:
   - ストレージ管理者 (`roles/storage.admin`)
   - Speech-to-Text 管理者 (`roles/speech.admin`)
   - Cloud Translation API ユーザー (`roles/cloudtranslate.user`)
   - Firestore ユーザー (`roles/datastore.user`)
6. 「続行」をクリックし、その後「完了」をクリック

## 3. サービスアカウントキーの作成とダウンロード

1. サービスアカウントページから、作成したサービスアカウントをクリック
2. 「鍵」タブに移動
3. 「鍵を追加」>「新しい鍵を作成」をクリック
4. キーのタイプとして「JSON」を選択
5. 「作成」をクリック
6. ダウンロードされたJSONキーファイルを安全な場所に保存

## 4. Cloud Storageバケットの設定

1. 以下のURLにアクセス: https://console.cloud.google.com/storage/browser
2. 「バケットを作成」をクリック
3. バケットの一意の名前を入力（例：`hippoapp-audio-storage`）
4. ロケーションタイプを選択（リージョンを推奨）
5. ユーザーに近いリージョンを選択（例：日本の場合は `asia-northeast1`）
6. ストレージクラスのデフォルト設定（標準）のままにする
7. アクセス制御のデフォルト設定（きめ細かい）のままにする
8. 「作成」をクリック

## 5. Firestoreデータベースの設定

1. 以下のURLにアクセス: https://console.cloud.google.com/firestore
2. 「データベースの作成」をクリック
3. 「ネイティブモード」を選択
4. ユーザーに近いロケーションを選択
5. 「作成」をクリック

## 6. 環境変数の設定

### Linux/Mac

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
```

### Windows (PowerShell)

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your-service-account-key.json"
```

## 7. 認証のテスト

1. プロジェクトディレクトリに移動
2. 認証テストを実行:

```bash
python demo.py --auth
```

成功すると、必要なすべてのサービスにアクセスできることが確認されます。

## 8. サンプル音声ファイルのアップロード

1. コンソールでCloud Storageバケットに移動
2. 「ファイルをアップロード」をクリック
3. テスト用の音声ファイルを選択
4. 「開く」をクリック

## 9. 文字起こしのテスト

```bash
python -m data-ingestion.scripts.transcribe --gcs-uri gs://your-bucket-name/your-audio-file.mp3 --output results.json
```

## 10. Webアプリケーションのテスト

```bash
python demo.py --web
```

## トラブルシューティング

### 認証の問題

- GOOGLE_APPLICATION_CREDENTIALS環境変数が正しく設定されていることを確認
- サービスアカウントに必要な権限があることを確認
- 必要なすべてのAPIが有効になっていることを確認

### APIクォータの制限

- クォータ制限に遭遇した場合、Google Cloud Consoleでクォータの増加をリクエストする必要があるかもしれません

### ストレージアクセスの問題

- バケットの権限を確認
- サービスアカウントにStorage Admin役割があることを確認

## 追加リソース

- [Google Cloud Speech-to-Text ドキュメント](https://cloud.google.com/speech-to-text/docs?hl=ja)
- [Google Cloud Translation ドキュメント](https://cloud.google.com/translate/docs?hl=ja)
- [Google Cloud Storage ドキュメント](https://cloud.google.com/storage/docs?hl=ja)
- [Firestore ドキュメント](https://cloud.google.com/firestore/docs?hl=ja)
