# 詳細なCloud Run公開アクセス設定ガイド

このガイドでは、Cloud Runサービスへの認証なしアクセスを設定する詳細な手順を説明します。

## 1. Google Cloud コンソールでの設定（最も簡単な方法）

1. [Google Cloud コンソール](https://console.cloud.google.com/)にアクセスします
2. 左側のナビゲーションメニューから「Cloud Run」を選択します
3. サービス一覧から「hippoapp」を選択します
4. 上部のタブから「権限」を選択します
5. 「プリンシパルを追加」ボタンをクリックします
6. 「新しいプリンシパル」フィールドに「allUsers」と入力します
7. 「ロール」ドロップダウンから「Cloud Run」カテゴリを選択し、「Cloud Run 起動元」を選択します
8. 「保存」をクリックします

これにより、認証なしでサービスにアクセスできるようになります。

## 2. gcloud コマンドラインでの設定

以下のコマンドを実行します:

```bash
gcloud run services add-iam-policy-binding hippoapp \
  --region=us-west1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

## 3. 組織ポリシーの確認と変更

もし上記の手順を実行しても403エラーが続く場合は、組織ポリシーの制限がある可能性があります。以下の手順で確認と変更を行います:

1. [Google Cloud コンソール](https://console.cloud.google.com/)にアクセスします
2. 左側のナビゲーションメニューから「IAMと管理」→「組織のポリシー」を選択します
3. 「iam.allowedPolicyMemberDomains」ポリシーを検索して選択します
4. 「ポリシーを編集」をクリックします
5. 「カスタマイズ」を選択します
6. 「ルールを追加」をクリックします
7. 「条件」セクションで、以下の条件を追加します:
   - 条件式: `resource.service == 'run.googleapis.com'`
   - タイトル: `Cloud Run services`
8. 「値」セクションで、「許可」を選択し、以下の値を追加します:
   - `allUsers`
   - `allAuthenticatedUsers`
9. 「保存」をクリックします

## 4. 設定の確認

設定が完了したら、以下のURLにアクセスして確認します:
https://hippoapp-546tyu2ata-uw.a.run.app

正常に設定されていれば、アプリケーションにアクセスできるようになります。

## トラブルシューティング

### 403 Forbidden エラーが続く場合

1. IAMポリシーが正しく適用されているか確認します:
   ```bash
   gcloud run services get-iam-policy hippoapp --region=us-west1
   ```

2. 組織ポリシーの制限がないか確認します:
   ```bash
   gcloud org-policies describe iam.allowedPolicyMemberDomains --effective
   ```

3. プロジェクト管理者に連絡し、組織ポリシーの変更権限があるか確認します

# Detailed Cloud Run Public Access Configuration Guide

This guide provides detailed instructions for configuring unauthenticated access to the Cloud Run service.

## 1. Configuration Using Google Cloud Console (Easiest Method)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select "Cloud Run" from the left navigation menu
3. Select the "hippoapp" service from the list
4. Click on the "Permissions" tab at the top
5. Click the "Add Principal" button
6. Enter "allUsers" in the "New principals" field
7. From the "Role" dropdown, select the "Cloud Run" category, then select "Cloud Run Invoker"
8. Click "Save"

This will allow unauthenticated access to the service.

## 2. Configuration Using gcloud Command Line

Run the following command:

```bash
gcloud run services add-iam-policy-binding hippoapp \
  --region=us-west1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

## 3. Checking and Modifying Organization Policy

If you still get 403 errors after following the above steps, there might be organization policy restrictions. Follow these steps to check and modify:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select "IAM & Admin" → "Organization policies" from the left navigation menu
3. Search for and select the "iam.allowedPolicyMemberDomains" policy
4. Click "Edit Policy"
5. Select "Customize"
6. Click "Add Rule"
7. In the "Condition" section, add the following condition:
   - Expression: `resource.service == 'run.googleapis.com'`
   - Title: `Cloud Run services`
8. In the "Values" section, select "Allow" and add the following values:
   - `allUsers`
   - `allAuthenticatedUsers`
9. Click "Save"

## 4. Verification

After configuring, verify by visiting:
https://hippoapp-546tyu2ata-uw.a.run.app

If configured correctly, you should be able to access the application.

## Troubleshooting

### If 403 Forbidden Errors Persist

1. Verify that the IAM policy has been correctly applied:
   ```bash
   gcloud run services get-iam-policy hippoapp --region=us-west1
   ```

2. Check if there are organization policy restrictions:
   ```bash
   gcloud org-policies describe iam.allowedPolicyMemberDomains --effective
   ```

3. Contact your project administrator to confirm you have permission to modify organization policies
