# ============================================================================
# COPY_TO_UE5_PROJECT.ps1
# ============================================================================
# PowerShell script to copy Najika implementation files to UE5 project
#
# USAGE:
#   .\COPY_TO_UE5_PROJECT.ps1 -ProjectPath "C:\Users\YourName\Documents\Unreal Projects\NajikaDigivice"
#
# REQUIREMENTS:
#   - PowerShell 5.1 or higher
#   - Target UE5 project must exist
#   - Run with Administrator privileges if needed for file operations
#
# Copyright Najika Development Team. All Rights Reserved.
# ============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath,

    [Parameter(Mandatory=$false)]
    [switch]$SkipBackup,

    [Parameter(Mandatory=$false)]
    [switch]$Force,

    [Parameter(Mandatory=$false)]
    [switch]$DocsOnly,

    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

# ============================================================================
# CONFIGURATION
# ============================================================================

$ErrorActionPreference = "Stop"
$ProgressPreference = "Continue"

# Source paths (relative to script location)
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourcePluginsDir = Join-Path $ScriptRoot "Plugins"
$SourceDocsDir = $ScriptRoot
$SourceTestsDir = Join-Path $ScriptRoot "Tests"

# Color output functions
function Write-Success { param([string]$Message) Write-Host "[SUCCESS] $Message" -ForegroundColor Green }
function Write-Info { param([string]$Message) Write-Host "[INFO] $Message" -ForegroundColor Cyan }
function Write-Warning { param([string]$Message) Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
function Write-Error { param([string]$Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }
function Write-Step { param([string]$Message) Write-Host "`n==> $Message" -ForegroundColor Magenta }

# ============================================================================
# VALIDATION
# ============================================================================

Write-Step "Validating Environment"

# Check PowerShell version
$PSVersion = $PSVersionTable.PSVersion
Write-Info "PowerShell Version: $PSVersion"
if ($PSVersion.Major -lt 5) {
    Write-Error "PowerShell 5.1 or higher required. Current: $PSVersion"
    exit 1
}

# Validate project path
if (-not (Test-Path $ProjectPath)) {
    Write-Error "Project path does not exist: $ProjectPath"
    exit 1
}

Write-Success "Project path exists: $ProjectPath"

# Check for .uproject file
$UProjectFiles = Get-ChildItem -Path $ProjectPath -Filter "*.uproject" -File
if ($UProjectFiles.Count -eq 0) {
    Write-Error "No .uproject file found in: $ProjectPath"
    exit 1
}

$UProjectFile = $UProjectFiles[0]
Write-Success "Found UE5 project file: $($UProjectFile.Name)"

# Validate source directories
if (-not (Test-Path $SourcePluginsDir)) {
    Write-Error "Source Plugins directory not found: $SourcePluginsDir"
    exit 1
}

Write-Success "Source directories validated"

# ============================================================================
# BACKUP EXISTING FILES
# ============================================================================

if (-not $SkipBackup) {
    Write-Step "Creating Backup"

    $BackupDir = Join-Path $ProjectPath "Backups"
    $BackupTimestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BackupPath = Join-Path $BackupDir "Backup_$BackupTimestamp"

    New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null

    # Backup existing Plugins directory if it exists
    $TargetPluginsDir = Join-Path $ProjectPath "Plugins"
    if (Test-Path $TargetPluginsDir) {
        Write-Info "Backing up existing Plugins directory..."
        $BackupPluginsDir = Join-Path $BackupPath "Plugins"
        Copy-Item -Path $TargetPluginsDir -Destination $BackupPluginsDir -Recurse -Force
        Write-Success "Backup created: $BackupPluginsDir"
    }

    Write-Success "Backup completed: $BackupPath"
} else {
    Write-Warning "Skipping backup (--SkipBackup flag set)"
}

# ============================================================================
# COPY PLUGINS
# ============================================================================

if (-not $DocsOnly) {
    Write-Step "Copying Plugins"

    $TargetPluginsDir = Join-Path $ProjectPath "Plugins"

    # Create Plugins directory if it doesn't exist
    if (-not (Test-Path $TargetPluginsDir)) {
        New-Item -ItemType Directory -Path $TargetPluginsDir -Force | Out-Null
        Write-Info "Created Plugins directory: $TargetPluginsDir"
    }

    # Plugin list
    $Plugins = @(
        "NajikaBackendClient",
        "NajikaVoiceSystem"
    )

    foreach ($Plugin in $Plugins) {
        Write-Info "Copying plugin: $Plugin"

        $SourcePluginDir = Join-Path $SourcePluginsDir $Plugin
        $TargetPluginDir = Join-Path $TargetPluginsDir $Plugin

        if (-not (Test-Path $SourcePluginDir)) {
            Write-Warning "Source plugin not found: $SourcePluginDir (skipping)"
            continue
        }

        # Check if target exists
        if ((Test-Path $TargetPluginDir) -and (-not $Force)) {
            $Response = Read-Host "Plugin '$Plugin' already exists. Overwrite? (y/N)"
            if ($Response -ne "y" -and $Response -ne "Y") {
                Write-Warning "Skipping $Plugin"
                continue
            }
        }

        # Copy plugin files
        Copy-Item -Path $SourcePluginDir -Destination $TargetPluginDir -Recurse -Force

        # Validate copy
        $UPluginFile = Join-Path $TargetPluginDir "$Plugin.uplugin"
        if (Test-Path $UPluginFile) {
            Write-Success "✓ $Plugin copied successfully"
        } else {
            Write-Error "✗ $Plugin copy failed (missing .uplugin file)"
        }
    }

    Write-Success "All plugins copied"
}

# ============================================================================
# COPY DOCUMENTATION
# ============================================================================

Write-Step "Copying Documentation"

$TargetDocsDir = Join-Path $ProjectPath "Documentation"
if (-not (Test-Path $TargetDocsDir)) {
    New-Item -ItemType Directory -Path $TargetDocsDir -Force | Out-Null
    Write-Info "Created Documentation directory: $TargetDocsDir"
}

# Documentation files to copy
$DocFiles = @(
    "BLUEPRINT_CREATION_GUIDE.md",
    "ASSET_REQUIREMENTS.md",
    "VISUAL_STUDIO_COMPILATION_GUIDE.md",
    "ANDROID_BUILD_GUIDE.md",
    "TESTING_CHECKLIST.md",
    "VOICE_BACKEND_API_SPEC.md",
    "IMPLEMENTATION_SUMMARY.md",
    "README.md"
)

foreach ($DocFile in $DocFiles) {
    $SourceDocPath = Join-Path $SourceDocsDir $DocFile
    $TargetDocPath = Join-Path $TargetDocsDir $DocFile

    if (Test-Path $SourceDocPath) {
        Copy-Item -Path $SourceDocPath -Destination $TargetDocPath -Force
        Write-Success "✓ Copied: $DocFile"
    } else {
        Write-Warning "✗ Not found: $DocFile (skipping)"
    }
}

Write-Success "Documentation copied"

# ============================================================================
# COPY TESTS (Optional)
# ============================================================================

if (Test-Path $SourceTestsDir) {
    Write-Step "Copying Tests"

    $TargetTestsDir = Join-Path $ProjectPath "Tests"
    if (-not (Test-Path $TargetTestsDir)) {
        New-Item -ItemType Directory -Path $TargetTestsDir -Force | Out-Null
    }

    Copy-Item -Path "$SourceTestsDir\*" -Destination $TargetTestsDir -Recurse -Force
    Write-Success "Tests copied"
}

# ============================================================================
# REGENERATE PROJECT FILES
# ============================================================================

Write-Step "Regenerating Project Files"

$UProjectPath = $UProjectFile.FullName
Write-Info "UProject file: $UProjectPath"

# Detect UE5 installation
$UE5Installations = @(
    "C:\Program Files\Epic Games\UE_5.3",
    "C:\Program Files\Epic Games\UE_5.2",
    "C:\Program Files\Epic Games\UE_5.1",
    "C:\Program Files\Epic Games\UE_5.0"
)

$UnrealVersionSelector = $null
foreach ($Installation in $UE5Installations) {
    $UVSPath = Join-Path $Installation "Engine\Binaries\Win64\UnrealVersionSelector.exe"
    if (Test-Path $UVSPath) {
        $UnrealVersionSelector = $UVSPath
        Write-Info "Found UnrealVersionSelector: $UVSPath"
        break
    }
}

if ($UnrealVersionSelector) {
    Write-Info "Regenerating Visual Studio project files..."

    try {
        & $UnrealVersionSelector /projectfiles $UProjectPath
        Write-Success "Project files regenerated successfully"
    } catch {
        Write-Warning "Failed to regenerate project files: $($_.Exception.Message)"
        Write-Info "You may need to right-click the .uproject file and select 'Generate Visual Studio project files'"
    }
} else {
    Write-Warning "UnrealVersionSelector not found"
    Write-Info "Manually regenerate project files:"
    Write-Info "  1. Right-click the .uproject file"
    Write-Info "  2. Select 'Generate Visual Studio project files'"
}

# ============================================================================
# SUMMARY
# ============================================================================

Write-Step "Installation Complete!"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  NAJIKA UE5 IMPLEMENTATION - INSTALLATION SUMMARY" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Success "Target Project: $ProjectPath"
Write-Success "Project File: $($UProjectFile.Name)"

Write-Host ""
Write-Host "INSTALLED COMPONENTS:" -ForegroundColor Yellow
if (-not $DocsOnly) {
    Write-Host "  ✓ NajikaBackendClient Plugin" -ForegroundColor Green
    Write-Host "  ✓ NajikaVoiceSystem Plugin" -ForegroundColor Green
}
Write-Host "  ✓ Documentation Files" -ForegroundColor Green
if (Test-Path $SourceTestsDir) {
    Write-Host "  ✓ Test Files" -ForegroundColor Green
}

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Open the project in Unreal Engine 5" -ForegroundColor White
Write-Host "  2. Go to Edit > Plugins and enable:" -ForegroundColor White
Write-Host "     - NajikaBackendClient" -ForegroundColor White
Write-Host "     - NajikaVoiceSystem" -ForegroundColor White
Write-Host "  3. Restart the editor when prompted" -ForegroundColor White
Write-Host "  4. Follow the BLUEPRINT_CREATION_GUIDE.md" -ForegroundColor White
Write-Host "  5. Refer to VISUAL_STUDIO_COMPILATION_GUIDE.md for C++ compilation" -ForegroundColor White
Write-Host ""

Write-Host "DOCUMENTATION LOCATION:" -ForegroundColor Yellow
Write-Host "  $TargetDocsDir" -ForegroundColor White
Write-Host ""

if (-not $SkipBackup) {
    Write-Host "BACKUP LOCATION:" -ForegroundColor Yellow
    Write-Host "  $BackupPath" -ForegroundColor White
    Write-Host ""
}

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Success "Installation script completed successfully!"
Write-Info "For questions or issues, refer to the documentation in: $TargetDocsDir"

# ============================================================================
# VERBOSE OUTPUT
# ============================================================================

if ($Verbose) {
    Write-Step "Verbose Output - File Structure"

    Write-Host "`nTarget Plugins Directory:" -ForegroundColor Yellow
    Get-ChildItem -Path $TargetPluginsDir -Recurse -File | ForEach-Object {
        Write-Host "  $($_.FullName.Replace($TargetPluginsDir, ''))" -ForegroundColor Gray
    }

    Write-Host "`nTarget Documentation Directory:" -ForegroundColor Yellow
    Get-ChildItem -Path $TargetDocsDir -File | ForEach-Object {
        Write-Host "  $($_.Name)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Info "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
