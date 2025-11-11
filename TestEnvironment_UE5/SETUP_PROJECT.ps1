# NAJIKA TEST ENVIRONMENT - AUTO SETUP SCRIPT (Windows)
# Model 2 - Test Environment Setup

Write-Host "🎮 NAJIKA TEST ENVIRONMENT - WINDOWS SETUP" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Target directory
$targetDir = "C:\NajikaTestEnvironment_UE5"

Write-Host "📍 Target Directory: $targetDir" -ForegroundColor Yellow
Write-Host ""

# Check if directory exists
if (Test-Path $targetDir) {
    Write-Host "⚠️  Directory already exists!" -ForegroundColor Red
    $response = Read-Host "Overwrite? (y/N)"

    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "❌ Setup cancelled." -ForegroundColor Red
        exit
    }

    Write-Host "🗑️  Removing old directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $targetDir
}

# Create directory structure
Write-Host "📁 Creating directory structure..." -ForegroundColor Green

New-Item -ItemType Directory -Force -Path "$targetDir\Source\NajikaTest\Public" | Out-Null
New-Item -ItemType Directory -Force -Path "$targetDir\Source\NajikaTest\Private" | Out-Null
New-Item -ItemType Directory -Force -Path "$targetDir\Config" | Out-Null
New-Item -ItemType Directory -Force -Path "$targetDir\Content\Maps" | Out-Null
New-Item -ItemType Directory -Force -Path "$targetDir\Content\Blueprints" | Out-Null
New-Item -ItemType Directory -Force -Path "$targetDir\Content\Materials" | Out-Null
New-Item -ItemType Directory -Force -Path "$targetDir\Docs" | Out-Null

Write-Host "✅ Directory structure created!" -ForegroundColor Green
Write-Host ""

# Copy files from git repo to target
$repoPath = $PSScriptRoot

Write-Host "📋 Copying project files..." -ForegroundColor Green

# Copy .uproject file
if (Test-Path "$repoPath\NajikaTest.uproject") {
    Copy-Item "$repoPath\NajikaTest.uproject" "$targetDir\" -Force
    Write-Host "  ✓ NajikaTest.uproject" -ForegroundColor Gray
}

# Copy Source files
if (Test-Path "$repoPath\Source\NajikaTest\Public\ExplosionClass.h") {
    Copy-Item "$repoPath\Source\NajikaTest\Public\ExplosionClass.h" "$targetDir\Source\NajikaTest\Public\" -Force
    Write-Host "  ✓ ExplosionClass.h" -ForegroundColor Gray
}

if (Test-Path "$repoPath\Source\NajikaTest\Private\ExplosionClass.cpp") {
    Copy-Item "$repoPath\Source\NajikaTest\Private\ExplosionClass.cpp" "$targetDir\Source\NajikaTest\Private\" -Force
    Write-Host "  ✓ ExplosionClass.cpp" -ForegroundColor Gray
}

# Copy Documentation
if (Test-Path "$repoPath\SETUP_WINDOWS.md") {
    Copy-Item "$repoPath\SETUP_WINDOWS.md" "$targetDir\Docs\" -Force
    Write-Host "  ✓ SETUP_WINDOWS.md" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ Files copied successfully!" -ForegroundColor Green
Write-Host ""

# Check for Unreal Engine
Write-Host "🔍 Checking for Unreal Engine 5.4..." -ForegroundColor Yellow

$ue5Path = "C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealEditor.exe"

if (Test-Path $ue5Path) {
    Write-Host "✅ Unreal Engine 5.4 found!" -ForegroundColor Green
    Write-Host ""

    $openProject = Read-Host "Open project in UE5? (Y/n)"

    if ($openProject -ne "n" -and $openProject -ne "N") {
        Write-Host "🚀 Launching Unreal Engine..." -ForegroundColor Cyan
        Start-Process $ue5Path -ArgumentList "`"$targetDir\NajikaTest.uproject`""
    }
} else {
    Write-Host "⚠️  Unreal Engine 5.4 not found!" -ForegroundColor Red
    Write-Host "   Please install from Epic Games Launcher" -ForegroundColor Yellow
    Write-Host "   https://www.epicgames.com/store/download" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Project Location: $targetDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Open NajikaTest.uproject in Unreal Editor" -ForegroundColor White
Write-Host "  2. Right-click .uproject → Generate Visual Studio files" -ForegroundColor White
Write-Host "  3. Build in Visual Studio (Ctrl+Shift+B)" -ForegroundColor White
Write-Host "  4. Create 10x10m Test Room in UE5" -ForegroundColor White
Write-Host "  5. Test Explosion Class!" -ForegroundColor White
Write-Host ""
Write-Host "📖 Documentation: $targetDir\Docs\SETUP_WINDOWS.md" -ForegroundColor Cyan
Write-Host ""
