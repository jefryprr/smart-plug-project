# 19 — Build Android APK

**Status:** `PASS: DEBUG_APK_BUILT` (not installed on a device)
**Yang sudah ada:** source `apps/android/App.tsx`, typecheck PASS, Expo Android bundle export PASS, debug APK 46,852,340 bytes, SHA-256 `BAFCD8BDD9EB0F79DD0807ABF73D5BBE8C42087E26AD69FB086E6976B30C2B61`.

## Prasyarat

- Android SDK di `D:\AI INSTALLS\Android\Sdk` (platform 36/37, build-tools 36/37, NDK 27.1.12297006).
- JDK 17.
- Gradle cache di `D:\AI INSTALLS\gradle`.

## Build

```powershell
cd apps\android
npm install
npx expo prebuild --platform android --no-install
cd android
.\gradlew.bat assembleDebug --console=plain "-PreactNativeArchitectures=arm64-v8a"
```

APK: `apps/android/android/app/build/outputs/apk/debug/app-debug.apk`.
Bukti build: `reports/ANDROID_BUILD.md`, `reports/logs/android-gradle-build.log`.

## Release

- Keystore terpisah, password di secret manager.
- Jangan commit keystore.
- EAS butuh akun/izin.

## Batas

- Debug APK `NOT_PRODUCTION`.
- BLE/push belum diimplementasikan.
- API base URL: emulator `10.0.2.2`, fisik IP LAN.
