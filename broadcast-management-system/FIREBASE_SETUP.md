# Firebase Configuration Guide

This guide explains how to set up Firebase for push notifications in the Broadcast Management System.

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: `broadcast-management`
4. Accept the default settings and create the project
5. Wait for project creation to complete

## Step 2: Set Up Cloud Messaging

### Enable Cloud Messaging
1. In Firebase Console, go to **Build** > **Cloud Messaging**
2. Click on **Get started** if not already enabled
3. Note the **Server API Key** and **Sender ID** (you'll need these)

## Step 3: Generate Service Account Key (for Backend)

1. Go to **Project Settings** (gear icon) > **Service Accounts**
2. Click **Generate New Private Key**
3. A JSON file will download
4. Copy the JSON content to `backend/firebase-service-account.json`

Example structure:
```json
{
  "type": "service_account",
  "project_id": "broadcast-management-xxxxx",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "firebase-adminsdk-xxxxx@broadcast-management-xxxxx.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

## Step 4: Android Configuration

### Download google-services.json

1. Go to **Project Overview** > **Add app** > **Android**
2. Enter package name: `com.broadcast.management`
3. Enter SHA-1 certificate (optional for development)
4. Download `google-services.json`
5. Place it in: `mobile/android/app/google-services.json`

### Update android/build.gradle

```gradle
buildscript {
  repositories {
    google()
    mavenCentral()
  }
  dependencies {
    classpath 'com.google.gms:google-services:4.3.15'
  }
}
```

### Update android/app/build.gradle

Add at the end of the file:
```gradle
apply plugin: 'com.google.gms.google-services'
```

## Step 5: iOS Configuration

### Download GoogleService-Info.plist

1. Go to **Project Overview** > **Add app** > **iOS**
2. Enter bundle ID: `com.broadcast.management`
3. Download `GoogleService-Info.plist`
4. Place it in: `mobile/ios/Runner/GoogleService-Info.plist`
5. Add to Xcode: Right-click on `ios/Runner` > **Add Files to Runner**

### Update iOS Deployment Target

In Xcode:
1. Select **Runner** project
2. Select **Runner** target
3. Set **Minimum Deployments** to **11.0** or higher

## Step 6: Backend Configuration

### Update .env

```bash
FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
```

### Verify Setup

Run the backend and check logs:
```bash
cd backend
python app.py
```

Look for: `Firebase initialized successfully` in the logs

## Step 7: Test Push Notifications

### Using Firebase Console

1. Go to **Cloud Messaging** > **Send your first message**
2. Enter notification title and content
3. Select **Send to specific topics** or **Send to specific devices**
4. Target your test device
5. Click **Send**

### From Backend API

Send a test broadcast:
```bash
curl -X POST http://localhost:5000/api/broadcasts \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Broadcast",
    "message": "This is a test notification"
  }'

# Send the broadcast
curl -X POST http://localhost:5000/api/broadcasts/1/send \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_users": [2, 3]}'
```

## Troubleshooting

### Issue: "Firebase not initialized"
- Ensure `firebase-service-account.json` exists in backend directory
- Check file path in `.env`
- Verify JSON is valid

### Issue: Android app not receiving notifications
- Verify `google-services.json` is in `android/app/`
- Check `android/build.gradle` has Firebase plugin
- Ensure app has notification permission
- Check logcat: `adb logcat | grep Firebase`

### Issue: iOS app not receiving notifications
- Verify `GoogleService-Info.plist` is added to Xcode project
- Check iOS deployment target is 11.0+
- Verify notification permission is granted
- Check Xcode console for Firebase errors

### Issue: Invalid Service Account Key
- Regenerate the key from Firebase Console
- Ensure JSON content is properly formatted
- Verify all required fields are present

## Production Checklist

- [ ] Use different Firebase projects for dev and production
- [ ] Restrict service account permissions in Firebase
- [ ] Store service account key securely (not in git)
- [ ] Monitor Firebase quota usage
- [ ] Set up Firebase Realtime Database backups
- [ ] Enable Firebase Security Rules
- [ ] Configure Firebase Custom Claims for advanced auth
- [ ] Set up Firebase Analytics
- [ ] Configure Firebase Crashlytics for error tracking

## Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [FCM Documentation](https://firebase.google.com/docs/cloud-messaging)
- [Firebase Flutter Integration](https://firebase.flutter.dev/)
- [Firebase Python Admin SDK](https://firebase.google.com/docs/admin/setup)
