# Initialize the portable ESP-IDF v6.1 environment without requiring the
# full `export.ps1` tool set (the repo does not install GDB, RISC-V, ULP tools).
#
# Dot-source this file:
#   . .\scripts\idf_env.ps1
#
# Requires ESP-IDF to be installed under tools\esp-idf (EIM or manual clone)
# and the ESP32-S3 toolchain under $env:IDF_TOOLS_PATH (default C:\Espressif).

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$idfPath = Join-Path $repoRoot "tools\esp-idf\v6.1\esp-idf"
if (-not (Test-Path (Join-Path $idfPath "tools\idf.py"))) {
    throw "ESP-IDF v6.1 not found at $idfPath"
}

if (-not $env:IDF_TOOLS_PATH) {
    $env:IDF_TOOLS_PATH = "C:\Espressif"
}
if (-not (Test-Path $env:IDF_TOOLS_PATH)) {
    throw "ESP-IDF tools path not found: $env:IDF_TOOLS_PATH"
}

$pythonEnv = Get-ChildItem (Join-Path $env:IDF_TOOLS_PATH "python_env") -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like "idf6.1*" } |
    Select-Object -First 1
if (-not $pythonEnv) {
    throw "ESP-IDF Python environment not found under $env:IDF_TOOLS_PATH\python_env"
}

$xtensa = Get-ChildItem (Join-Path $env:IDF_TOOLS_PATH "tools\xtensa-esp-elf") -Directory -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $xtensa) {
    throw "xtensa-esp-elf toolchain not found under $env:IDF_TOOLS_PATH\tools"
}

$cmake = Get-ChildItem (Join-Path $env:IDF_TOOLS_PATH "tools\cmake") -Directory -ErrorAction SilentlyContinue |
    Select-Object -First 1
$ninja = Get-ChildItem (Join-Path $env:IDF_TOOLS_PATH "tools\ninja") -Directory -ErrorAction SilentlyContinue |
    Select-Object -First 1
$ccache = Get-ChildItem (Join-Path $env:IDF_TOOLS_PATH "tools\ccache") -File -Recurse -Filter "ccache.exe" -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $cmake -or -not $ninja) {
    throw "cmake/ninja not found under $env:IDF_TOOLS_PATH\tools"
}

$romElfs = Get-ChildItem (Join-Path $env:IDF_TOOLS_PATH "tools\esp-rom-elfs") -Directory -ErrorAction SilentlyContinue |
    Select-Object -First 1

$env:IDF_PATH = $idfPath
$env:IDF_PYTHON_ENV_PATH = $pythonEnv.FullName
$env:ESP_IDF_VERSION = "6.1"
$env:PYTHONUTF8 = "1"
if ($romElfs) {
    $env:ESP_ROM_ELF_DIR = $romElfs.FullName
}
$extraPaths = @(
    (Join-Path $pythonEnv.FullName "Scripts"),
    (Join-Path $xtensa.FullName "xtensa-esp-elf\bin"),
    (Join-Path $cmake.FullName "bin"),
    $ninja.FullName
)
if ($ccache) {
    $extraPaths += $ccache.DirectoryName
    if (-not $env:CCACHE_DIR) { $env:CCACHE_DIR = "D:\AI INSTALLS\ccache" }
}
$env:PATH = ($extraPaths + $env:PATH) -join ";"

$idfPy = Join-Path $env:IDF_PYTHON_ENV_PATH "Scripts\python.exe"
if (-not (Test-Path $idfPy)) {
    throw "ESP-IDF Python not found: $idfPy"
}

Write-Host "ESP-IDF environment ready: $env:ESP_IDF_VERSION at $env:IDF_PATH"
