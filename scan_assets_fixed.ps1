# ===============================================
# NAJIKA WORLD - ASSET STRUCTURE SCANNER
# ===============================================
# Scannt die gesamte Asset-Ordnerstruktur und erstellt Dokumentation
#
# USAGE:
#   PowerShell: .\scan_assets_fixed.ps1
#   Output: ASSET_STRUCTURE.md
#
# Author: Claude Code
# Date: 2025-11-05
# ===============================================

$ErrorActionPreference = "Continue"
$OutputFile = "ASSET_STRUCTURE.md"

# Bestimme Asset-Pfad
$AssetPath = Join-Path $PSScriptRoot "assets"

if (-not (Test-Path $AssetPath)) {
    Write-Host "ERROR: Asset folder not found at: $AssetPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure assets are located at:" -ForegroundColor Yellow
    Write-Host "  Windows: C:\Najika-World\assets\" -ForegroundColor Yellow
    Write-Host "  Linux: /home/user/Najika_World/assets/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Scanning Asset Structure..." -ForegroundColor Cyan
Write-Host "Path: $AssetPath" -ForegroundColor Gray
Write-Host ""

# Initialisiere Markdown Output
$Output = @"
# NAJIKA WORLD - ASSET STRUCTURE
**Generated:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

---

## OVERVIEW

"@

# Zaehle Dateien und Groesse
Write-Host "Calculating statistics..." -ForegroundColor Cyan
$AllFiles = Get-ChildItem -Path $AssetPath -Recurse -File -ErrorAction SilentlyContinue
$TotalFiles = $AllFiles.Count
$TotalSize = ($AllFiles | Measure-Object -Property Length -Sum).Sum
$TotalSizeGB = [math]::Round($TotalSize / 1GB, 2)

# Zaehle Ordner
$AllFolders = Get-ChildItem -Path $AssetPath -Recurse -Directory -ErrorAction SilentlyContinue
$TotalFolders = $AllFolders.Count

$Output += @"
- **Total Folders:** $TotalFolders
- **Total Files:** $TotalFiles
- **Total Size:** $TotalSizeGB GB

---

## FILE TYPES

"@

# Gruppiere nach Dateityp
$FileTypes = $AllFiles | Group-Object Extension | Sort-Object Count -Descending
$Output += @"
| Extension | Count | Example |
|-----------|-------|---------|

"@

foreach ($Type in $FileTypes) {
    $ExtName = if ($Type.Name) { $Type.Name } else { "(no extension)" }
    $ExampleFile = ($Type.Group | Select-Object -First 1).Name
    $Output += "| ``$ExtName`` | $($Type.Count) | $ExampleFile |`n"
}

$Output += @"

---

## FOLDER STRUCTURE

"@

# Funktion zum Erstellen der Baumstruktur (ASCII only!)
function Get-FolderTree {
    param(
        [string]$Path,
        [int]$Level = 0,
        [string]$Prefix = ""
    )

    $Items = Get-ChildItem -Path $Path -ErrorAction SilentlyContinue | Sort-Object { $_.PSIsContainer } -Descending
    $ItemCount = $Items.Count
    $CurrentItem = 0

    foreach ($Item in $Items) {
        $CurrentItem++
        $IsLast = ($CurrentItem -eq $ItemCount)

        if ($IsLast) {
            $Branch = "+-- "
            $NextPrefix = $Prefix + "    "
        } else {
            $Branch = "+-- "
            $NextPrefix = $Prefix + "|   "
        }

        if ($Item.PSIsContainer) {
            # Ordner
            $FolderFiles = (Get-ChildItem -Path $Item.FullName -Recurse -File -ErrorAction SilentlyContinue).Count
            $OutputLine = "$Prefix$Branch$($Item.Name)/ ($FolderFiles files)`n"
            Write-Output $OutputLine

            # Rekursiv in Unterordner (max 4 Ebenen tief)
            if ($Level -lt 4) {
                Get-FolderTree -Path $Item.FullName -Level ($Level + 1) -Prefix $NextPrefix
            }
        } else {
            # Datei
            $FileSize = [math]::Round($Item.Length / 1MB, 2)
            $OutputLine = "$Prefix$Branch$($Item.Name) ($FileSize MB)`n"
            Write-Output $OutputLine
        }
    }
}

Write-Host "Building folder tree..." -ForegroundColor Cyan
$Output += "``````text`n"
$Output += "assets/`n"
$Output += Get-FolderTree -Path $AssetPath
$Output += "``````"

$Output += @"


---

## KAYKIT PACKS DETECTED

"@

# Suche nach KayKit Packs
$KayKitPacks = Get-ChildItem -Path $AssetPath -Directory -Filter "KayKit*" -ErrorAction SilentlyContinue

if ($KayKitPacks.Count -gt 0) {
    $Output += "| Pack Name | Files | Size (GB) | Status |`n"
    $Output += "|-----------|-------|-----------|--------|`n"

    foreach ($Pack in $KayKitPacks) {
        $PackFiles = (Get-ChildItem -Path $Pack.FullName -Recurse -File -ErrorAction SilentlyContinue)
        $PackSize = ($PackFiles | Measure-Object -Property Length -Sum).Sum
        $PackSizeGB = [math]::Round($PackSize / 1GB, 2)
        $FileCount = $PackFiles.Count

        $Status = if ($FileCount -gt 0) { "OK" } else { "Empty" }

        $Output += "| ``$($Pack.Name)`` | $FileCount | $PackSizeGB | $Status |`n"
    }
} else {
    $Output += "No KayKit packs found. Please ensure assets are properly installed.`n`n"
    $Output += "Expected packs:`n"
    $Output += "- KayKit_DungeonRemastered_1.1_FREE`n"
    $Output += "- KayKit_Skeletons_1.0_FREE`n"
    $Output += "- KayKit_Adventurers_1.0_FREE`n"
    $Output += "- KayKit_FurnitureBits_1.0_FREE`n"
    $Output += "- KayKit_RestaurantBits_1.0_FREE`n"
    $Output += "- KayKit_HalloweenBits_1.0_FREE`n"
}

$Output += @"


---

## CONFIG FILES

"@

# Suche nach Config-Dateien
$ConfigFiles = Get-ChildItem -Path $AssetPath -Filter "*.json" -ErrorAction SilentlyContinue

if ($ConfigFiles.Count -gt 0) {
    $Output += "| File | Size | Status |`n"
    $Output += "|------|------|--------|`n"

    foreach ($Config in $ConfigFiles) {
        $ConfigSize = [math]::Round($Config.Length / 1KB, 2)
        $Status = "Found"
        $Output += "| ``$($Config.Name)`` | $ConfigSize KB | $Status |`n"
    }
} else {
    $Output += "No config files found!`n`n"
    $Output += "Expected: ``room_config_detailed.json```n"
}

$Output += @"


---

## NOTES

- This structure was automatically generated by scan_assets_fixed.ps1
- All KayKit assets are CC0 licensed (free to use!)
- Assets are excluded from GitHub due to size (see .gitignore)
- For asset installation instructions, see: ASSETS_DOWNLOAD.md

---

**Generated by:** Claude Code
**Project:** Najika World
**Date:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

"@

# Schreibe Output in Datei
$Output | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host ""
Write-Host "Asset structure documented!" -ForegroundColor Green
Write-Host "Output: $OutputFile" -ForegroundColor Gray
Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "Folders: $TotalFolders" -ForegroundColor Gray
Write-Host "Files: $TotalFiles" -ForegroundColor Gray
Write-Host "Size: $TotalSizeGB GB" -ForegroundColor Gray
Write-Host ""
