> **REV_D note:** the existing debug APK predates the CORE-only time-status UI. `npm run typecheck` passes; rebuild/device test is required before using the APK as evidence for REV_D.

# Android Debug APK — Build Evidence

**Status:** `PASS` (debug APK built and signature-verified)
**Date:** 2026-11-15
**App:** `com.smartplug.demo` version 0.1.0 (versionCode 1)
**APK:** `apps/android/android/app/build/outputs/apk/debug/app-debug.apk`
**Mirror:** `D:\AI INSTALLS\artifacts\smartplug-debug.apk`
**Size:** 46,852,340 bytes
**SHA-256:** `BAFCD8BDD9EB0F79DD0807ABF73D5BBE8C42087E26AD69FB086E6976B30C2B61`
**Log:** `reports/logs/android-gradle-build.log`

## Toolchain

| Item | Value |
|---|---|
| Expo SDK | 58.0.25 |
| React Native | 0.88.1 |
| Gradle | 9.4.1 |
| AGP | from Expo 58 / RN 0.88 template |
| JDK | Microsoft OpenJDK 17.0.10.7 |
| Android SDK | `D:\AI INSTALLS\Android\Sdk` |
| compileSdk | 37 |
| targetSdk | 36 |
| minSdk | 24 |
| Build tools | 37.0.0 (Gradle installed it; 36.0.0 also present) |
| NDK | 27.1.12297006 |
| CMake | 3.22.1 |
| ABI | `arm64-v8a` only (explicitly limited for this debug build) |
| Gradle cache | `D:\AI INSTALLS\gradle` |

## Commands

```powershell
cd apps\android
npm install
npx expo prebuild --platform android --no-install

$env:ANDROID_HOME = "D:\AI INSTALLS\Android\Sdk"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:JAVA_HOME = "C:\Users\<user>\AppData\Local\Programs\Microsoft\jdk-17.0.10.7-hotspot"
$env:GRADLE_USER_HOME = "D:\AI INSTALLS\gradle"
cd android
.\gradlew.bat assembleDebug --console=plain "-PreactNativeArchitectures=arm64-v8a"
```

The build finished with `BUILD SUCCESSFUL in 21m 17s` (232 tasks).

## Verification

```text
package: name='com.smartplug.demo' versionCode='1' versionName='0.1.0'
minSdkVersion:'24'
targetSdkVersion:'36'
compileSdkVersion='37'
```

`apksigner verify --verbose`:

```text
Verifies
Verified using v2 scheme (APK Signature Scheme v2): true
Number of signers: 1
```

The signature is the **debug** key, not a production/release key.

## What this proves

- The Expo/React Native Android project prebuilds and compiles for `arm64-v8a`.
- The debug APK is structurally valid and signature-verifies with the debug key.
- The APK contains `INTERNET` permission and the app package name.

## What this does **not** prove

- It was not installed on a device or emulator.
- No UI/API/MQTT interaction was tested on Android.
- It is not a release build, not release-signed, and not Play-Store ready.
- It is `arm64-v8a` only; x86/x86_64/armeabi-v7a are not in this APK.
- It uses a debug manifest with `usesCleartextTraffic` for the local HTTP API.
- BLE provisioning, push, and production API/TLS configuration are absent.

## Notes and warnings

- Gradle/Expo/RN emitted deprecation warnings (AGP legacy variant API, Kotlin,
  `NativeArrayBuffer`, Gradle 10 incompatibility). The build succeeds, but the
  stack should be pinned/updated before production.
- Android SDK 37/build-tools 37 were installed automatically by Gradle even
  though 36 was preinstalled. The exact versions are recorded above.
- `SYSTEM_ALERT_WINDOW` and legacy storage permissions appear in the debug
  manifest from the Expo/RN dev client. They are not a production permission
  review.

**Safety:** Android build PASS has no bearing on mains safety. The debug APK is
`NOT_PRODUCTION`.
