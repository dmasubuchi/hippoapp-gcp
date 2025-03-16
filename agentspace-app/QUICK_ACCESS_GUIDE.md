# Cloud Run 公開アクセス設定クイックガイド

## Google Cloud コンソールでの設定（最速）

1. [Google Cloud コンソール](https://console.cloud.google.com/)にアクセス
2. 「Cloud Run」→「hippoapp」→「権限」タブ
3. 「プリンシパルを追加」→「allUsers」→「Cloud Run 起動元」ロール
4. 「保存」をクリック

## 確認方法

設定後、以下のURLにアクセス:
https://hippoapp-546tyu2ata-uw.a.run.app

# Cloud Run Public Access Quick Guide

## Configure in Google Cloud Console (Fastest)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "Cloud Run" → "hippoapp" → "Permissions" tab
3. "Add Principal" → "allUsers" → "Cloud Run Invoker" role
4. Click "Save"

## Verification

After configuring, visit:
https://hippoapp-546tyu2ata-uw.a.run.app
