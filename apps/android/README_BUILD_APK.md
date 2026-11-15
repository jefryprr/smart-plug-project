# Build APK — Smart Plug Android

**Status lingkungan saat ini:** `PASS: DEBUG_APK_BUILT` (signature verified; not installed/tested on device)
**Artefak APK:** `apps/android/android/app/build/outputs/apk/debug/app-debug.apk` — 46,852,340 bytes, SHA-256 `BAFCD8BDD9EB0F79DD0807ABF73D5BBE8C42087E26AD69FB086E6976B30C2B61`.

Aplikasi memakai React Native + Expo (SDK 58) dengan development build. Sumber ada di `apps/android/App.tsx`.

## Prasyarat

| Kebutuhan | Versi/status |
|---|---|
| Node.js | 24.x (tersedia) |
| JDK | 17 (tersedia) |
| Android SDK Platform | 36/37 (terpasang di D:) |
| Android Build Tools | 36.0.0/37.0.0 (terpasang di D:) |
| NDK | 27.1.12297006 (terpasang) |
| adb | platform-tools terpasang; emulator belum diuji |
| Expo CLI | melalui `npx expo` (paket lokal) |

Android SDK dipasang di `D:\AI INSTALLS\Android\Sdk`, Gradle cache di
`D:\AI INSTALLS\gradle`. Jangan menaruh path SDK absolut di source atau commit
`local.properties`.

## Build lokal (debug)

```powershell
cd apps/android
npm install
npx expo prebuild --platform android
npx expo run:android
```

Alternatif setelah prebuild:

```powershell
$env:ANDROID_HOME = "D:\AI INSTALLS\Android\Sdk"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:JAVA_HOME = "C:\Users\<user>\AppData\Local\Programs\Microsoft\jdk-17.0.10.7-hotspot"
$env:GRADLE_USER_HOME = "D:\AI INSTALLS\gradle"
cd apps/android/android
.\gradlew.bat assembleDebug --console=plain "-PreactNativeArchitectures=arm64-v8a"
```

Build evidence: `reports/ANDROID_BUILD.md`, `reports/logs/android-gradle-build.log`.

APK debug yang diharapkan:

```text
apps/android/android/app/build/outputs/apk/debug/app-debug.apk
```

Debug APK diberi label **NOT_PRODUCTION**. Debug signing bukan release signing.
The APK was built for `arm64-v8a` only and has not been installed on a device or emulator.

## Build release

Release memerlukan keystore terpisah, password, dan persetujuan pemilik. Jangan commit keystore atau password. Buat keystore di lokasi aman di luar repo, lalu konfigurasikan lewat environment/secret manager. EAS build memerlukan akun Expo dan persetujuan; jangan mengaktifkan layanan berbayar tanpa izin.

## Menjalankan aplikasi

1. Jalankan API: `npm run dev:api` dari root repo.
2. Jalankan broker MQTT + device simulator bila ingin menguji perintah:
   - broker: Mosquitto/Aedes pada port 1883 atau gunakan `scripts/e2e_api.mjs` sebagai contoh stack.
   - simulator: `npm run sim:dev`.
3. Emulator Android memakai API base URL `http://10.0.2.2:4000`.
4. Perangkat fisik memakai IP LAN komputer, misalnya `http://192.168.1.10:4000`; pastikan firewall mengizinkan port 4000 pada jaringan lokal tepercaya.
5. Login demo: `demo@example.com` / `demo1234` (hanya seed lokal).

## Batasan yang harus dipertahankan

- BLE provisioning dan pairing perangkat belum diimplementasikan di aplikasi; pairing saat ini melalui kode di web/API.
- Push notification Android (FCM/Expo) belum diaktifkan. Test notification memakai endpoint backend.
- Aplikasi tidak menampilkan status fisik OFF tanpa sensor feedback; `observed_output` null berarti tidak terverifikasi.
- Jangan menulis SSID/password Wi-Fi atau token ke log/analytics.
- Token disimpan di SecureStore; untuk produksi, tambahkan rotasi refresh token dan revoke sesi.
- Aplikasi ini bukan alat ukur resmi dan bukan pengganti proteksi listrik.

## Log build yang harus disimpan

Simpan output `npx expo run:android` atau `gradlew assembleDebug` ke `reports/logs/` dan catat:

- versi Expo/React Native/Gradle/AGP,
- hash commit,
- path APK,
- ukuran dan SHA-256,
- hasil instalasi di emulator/perangkat,
- kegagalan yang tersisa.

Tanpa log tersebut, status build tetap `UNVERIFIED`/`BLOCKED`.
