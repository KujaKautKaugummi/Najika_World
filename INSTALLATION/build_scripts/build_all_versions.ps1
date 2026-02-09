# ============================================================
# Najika Digivice - Build All Versions Script (Windows)
# ============================================================
# This script builds all 3 versions of the Digivice app:
# 1. Master Edition (Najika)
# 2. Trusted Edition (Friends)
# 3. Public Edition
#
# Usage: .\build_all_versions.ps1
# ============================================================

# Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Join-Path $ScriptDir "..\flutter_app\najika_digivice"
$OutputDir = Join-Path $ScriptDir "builds"
$BuildConfig = Join-Path $ProjectDir "lib\config\build_config.dart"

# Create output directory
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

# ============================================================
# Helper Functions
# ============================================================

function Print-Header {
    param([string]$Message)
    Write-Host "============================================================" -ForegroundColor Blue
    Write-Host $Message -ForegroundColor Blue
    Write-Host "============================================================" -ForegroundColor Blue
}

function Print-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Print-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Print-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Yellow
}

# ============================================================
# Build Configuration Switcher
# ============================================================

function Set-BuildEdition {
    param([string]$Edition)

    Print-Info "Setting build edition to: $Edition"

    # Backup original
    Copy-Item $BuildConfig "$BuildConfig.bak" -Force

    # Read file content
    $content = Get-Content $BuildConfig -Raw

    # Replace edition
    switch ($Edition) {
        "master" {
            $content = $content -replace 'static const DigiviceEdition edition = DigiviceEdition\.[a-z]*;', 'static const DigiviceEdition edition = DigiviceEdition.master;'
        }
        "trusted" {
            $content = $content -replace 'static const DigiviceEdition edition = DigiviceEdition\.[a-z]*;', 'static const DigiviceEdition edition = DigiviceEdition.trusted;'
        }
        "public" {
            $content = $content -replace 'static const DigiviceEdition edition = DigiviceEdition\.[a-z]*;', 'static const DigiviceEdition edition = DigiviceEdition.public;'
        }
        default {
            Print-Error "Unknown edition: $Edition"
            exit 1
        }
    }

    # Write back
    Set-Content $BuildConfig $content -NoNewline

    Print-Success "Build edition set to: $Edition"
}

function Restore-BuildConfig {
    if (Test-Path "$BuildConfig.bak") {
        Move-Item "$BuildConfig.bak" $BuildConfig -Force
        Print-Info "Restored original build_config.dart"
    }
}

# ============================================================
# Build Function
# ============================================================

function Build-Version {
    param(
        [string]$Edition,
        [string]$OutputName
    )

    Print-Header "Building $Edition Edition"

    # Set build edition
    Set-BuildEdition $Edition

    # Navigate to project
    Set-Location $ProjectDir

    # Clean previous builds
    Print-Info "Cleaning previous builds..."
    flutter clean | Out-Null

    # Get dependencies
    Print-Info "Getting dependencies..."
    flutter pub get | Out-Null

    # Build APK
    Print-Info "Building APK..."
    flutter build apk --release

    # Copy APK to output directory
    $apkPath = Join-Path $ProjectDir "build\app\outputs\flutter-apk\app-release.apk"
    if (Test-Path $apkPath) {
        $outputPath = Join-Path $OutputDir $OutputName
        Copy-Item $apkPath $outputPath -Force
        Print-Success "APK built successfully: $OutputName"

        # Get APK size
        $size = (Get-Item $outputPath).Length / 1MB
        Print-Info ("APK size: {0:N2} MB" -f $size)
    } else {
        Print-Error "APK not found at: $apkPath"
        return $false
    }

    # Restore build config
    Restore-BuildConfig

    Write-Host ""
    return $true
}

# ============================================================
# Main Build Process
# ============================================================

Print-Header "Najika Digivice - Build All Versions"

# Check if Flutter is installed
if (-not (Get-Command flutter -ErrorAction SilentlyContinue)) {
    Print-Error "Flutter is not installed or not in PATH"
    exit 1
}

Print-Info "Flutter version:"
flutter --version

Write-Host ""

# Ask user which versions to build
Write-Host "Which versions do you want to build?" -ForegroundColor Yellow
Write-Host "1) All versions"
Write-Host "2) Master only"
Write-Host "3) Trusted only"
Write-Host "4) Public only"
Write-Host "5) Master + Trusted"
$choice = Read-Host "Enter choice (1-5)"

switch ($choice) {
    "1" {
        # Build all versions
        Build-Version "master" "najika_digivice_master.apk"
        Build-Version "trusted" "najika_digivice_trusted.apk"
        Build-Version "public" "najika_digivice_public.apk"
    }
    "2" {
        Build-Version "master" "najika_digivice_master.apk"
    }
    "3" {
        Build-Version "trusted" "najika_digivice_trusted.apk"
    }
    "4" {
        Build-Version "public" "najika_digivice_public.apk"
    }
    "5" {
        Build-Version "master" "najika_digivice_master.apk"
        Build-Version "trusted" "najika_digivice_trusted.apk"
    }
    default {
        Print-Error "Invalid choice"
        exit 1
    }
}

# ============================================================
# Summary
# ============================================================

Print-Header "Build Summary"

Write-Host "Built APKs:" -ForegroundColor Green
Get-ChildItem $OutputDir -Filter *.apk | Format-Table Name, @{Name="Size (MB)";Expression={"{0:N2}" -f ($_.Length / 1MB)}}

Write-Host ""
Print-Success "All builds completed!"
Print-Info "APKs saved to: $OutputDir"

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Master Edition → Install on your phone"
Write-Host "2. Trusted Edition → Send to friends"
Write-Host "3. Public Edition → Test before App Store submission"

Write-Host ""
Write-Host "Installation:" -ForegroundColor Blue
Write-Host "adb install $OutputDir\najika_digivice_master.apk"

# ============================================================
# Cleanup
# ============================================================

# Ensure build config is restored
Restore-BuildConfig

# Return to script directory
Set-Location $ScriptDir

Print-Success "Done!"
