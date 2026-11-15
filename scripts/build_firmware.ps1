# Build the ESP-IDF firmware for ESP32-S3 and write a reproducible log.
# Run from the repository root:
#   powershell -ExecutionPolicy Bypass -File scripts\build_firmware.ps1

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "idf_env.ps1")

$idfPy = Join-Path $env:IDF_PYTHON_ENV_PATH "Scripts\python.exe"
$idf = Join-Path $env:IDF_PATH "tools\idf.py"
$logDir = Join-Path $repoRoot "reports\logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir "firmware-idf-build.log"
if (Test-Path $log) { Remove-Item $log -Force }

# A failed CMake configure can leave a non-CMake build directory that
# `idf.py set-target` refuses to clean. Remove it so this is a true rebuild.
$buildDir = Join-Path $repoRoot "firmware\build"
if (Test-Path $buildDir) { Remove-Item -Recurse -Force $buildDir }

Push-Location (Join-Path $repoRoot "firmware")
try {
    # Use cmd.exe for redirection so native stderr (including benign Kconfig
    # warnings) is not converted into a terminating PowerShell error.
    Write-Host "== idf.py set-target esp32s3 =="
    $setTarget = "`"$idfPy`" `"$idf`" set-target esp32s3 > `"$log`" 2>&1"
    & cmd.exe /d /c $setTarget
    $setTargetCode = $LASTEXITCODE
    Get-Content $log -Tail 40 -ErrorAction SilentlyContinue | Write-Host
    if ($setTargetCode -ne 0) { throw "set-target failed with exit code $setTargetCode" }

    Write-Host "== idf.py build =="
    $build = "`"$idfPy`" `"$idf`" build >> `"$log`" 2>&1"
    & cmd.exe /d /c $build
    $buildCode = $LASTEXITCODE
    Get-Content $log -Tail 60 -ErrorAction SilentlyContinue | Write-Host
    if ($buildCode -ne 0) { throw "build failed with exit code $buildCode" }
}
finally {
    Pop-Location
}

$bin = Join-Path $repoRoot "firmware\build\smartplug.bin"
if (-not (Test-Path $bin)) {
    throw "Build reported success but $bin is missing"
}
$size = (Get-Item $bin).Length
Write-Host "BUILD_OK smartplug.bin bytes=$size"
exit 0
