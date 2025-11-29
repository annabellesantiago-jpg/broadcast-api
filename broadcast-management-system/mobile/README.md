# Broadcast Management Mobile App

A Flutter mobile application for the Broadcast Management System with push notification support.

## Features

- User authentication (login/signup)
- Receive push notifications
- View all received broadcasts
- Real-time notification updates
- Offline support with local storage

## Getting Started

### Prerequisites

- Flutter SDK (^3.0.0)
- Android Studio or Xcode
- Firebase account

### Setup

1. Clone and navigate to the mobile directory:
```bash
cd mobile
```

2. Get dependencies:
```bash
flutter pub get
```

3. Configure Firebase:
   - Create a Firebase project
   - Download google-services.json (Android) and GoogleService-Info.plist (iOS)
   - Place them in the respective platform directories

4. Run the app:
```bash
flutter run
```

## Firebase Setup

### Android

1. Copy `google-services.json` to `android/app/`
2. Update `android/build.gradle` with Firebase plugin

### iOS

1. Copy `GoogleService-Info.plist` to `ios/Runner/`
2. Update `ios/Podfile` for Firebase

## Project Structure

```
lib/
├── main.dart              # App entry point
├── screens/               # UI screens
│   ├── login_screen.dart
│   ├── signup_screen.dart
│   └── home_screen.dart
├── services/              # Business logic
│   ├── api_service.dart
│   └── notification_service.dart
└── models/                # Data models
    ├── user.dart
    └── broadcast.dart
```
