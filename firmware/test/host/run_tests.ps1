$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
$zig = Join-Path $root "tools\zig\zig-x86_64-windows-0.17.1\zig.exe"
$build = Join-Path $PSScriptRoot "build"
$logDir = Join-Path $root "reports\logs"
New-Item -ItemType Directory -Force -Path $build, $logDir | Out-Null

if (-not (Test-Path $zig)) {
    Write-Error "Zig compiler not found at $zig. See docs/tutorials/14_SETUP_ESP_IDF.md for host-test prerequisites."
}

$env:PATH = (Split-Path $zig -Parent) + ";" + $env:PATH

& $zig cc -std=c99 -Wall -Wextra -Werror `
    -I (Join-Path $root "firmware\core\include") `
    (Join-Path $root "firmware\core\smartplug_core.c") `
    (Join-Path $PSScriptRoot "test_core.c") `
    -o (Join-Path $build "test_core.exe") -lm 2>&1 |
    Tee-Object -FilePath (Join-Path $logDir "firmware-host-build.log")

if ($LASTEXITCODE -ne 0) {
    Write-Error "Host core build failed with exit code $LASTEXITCODE"
}

& (Join-Path $build "test_core.exe") 2>&1 |
    Tee-Object -FilePath (Join-Path $logDir "firmware-host-test.log")

if ($LASTEXITCODE -ne 0) {
    Write-Error "Host core tests failed with exit code $LASTEXITCODE"
}

Write-Output "Firmware host core tests PASS"
