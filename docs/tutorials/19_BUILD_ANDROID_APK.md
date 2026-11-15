# 19 — Build Android APK

**Status:** `BLOCKED: ANDROID_SDK_NOT_INSTALLED`
**Yang sudah ada:** source `apps/android/App.tsx`, typecheck PASS, Expo Android bundle export PASS. **APK belum ada.**

## Prasyarat

- Android Studio/SDK, platform 35/36, build-tools, adb/emulator.
- JDK 17.

## Build

```powershell
cd apps\android
npm install
npx expo prebuild --platform android
npx expo run:android
```

Atau:
```powershell
cd apps\android\android
.\gradlew.bat assembleDebug
```

APK: `apps/android/android/app/build/outputs/apk/debug/app-debug.apk`.

## Release

- Keystore terpisah, password di secret manager.
- Jangan commit keystore.
- EAS butuh akun/izin.

## Batas

- Debug APK `NOT_PRODUCTION`.
- BLE/push belum diimplementasikan.
- API base URL: emulator `10.0.2.2`, fisik IP LAN.
