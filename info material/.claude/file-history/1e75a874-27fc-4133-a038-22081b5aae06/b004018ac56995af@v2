# Claude Code Status Line - Windows Configuration
# Reads JSON input from stdin and displays: timestamp | cwd | git branch | model

$input = [Console]::In.ReadToEnd()
$json = $input | ConvertFrom-Json

# Extract current directory
$cwd = $json.workspace.current_dir
if (-not $cwd) { $cwd = $json.cwd }

# Simplify path - show only last 2 directories
$cwdParts = $cwd -split '\\'
if ($cwdParts.Length -gt 2) {
    $shortCwd = "...\" + ($cwdParts[-2..-1] -join '\')
} else {
    $shortCwd = $cwd
}

# Get timestamp
$timestamp = Get-Date -Format "HH:mm:ss"

# Get git branch (if in a repo)
$gitBranch = ""
try {
    Push-Location $cwd
    $branch = git rev-parse --abbrev-ref HEAD 2>$null
    if ($LASTEXITCODE -eq 0 -and $branch) {
        $gitBranch = " [git:$branch]"
    }
    Pop-Location
} catch {
    # Not a git repo or git not available
}

# Get model name
$modelName = $json.model.display_name
if (-not $modelName) { $modelName = $json.model.id }

# Build status line
Write-Host "$timestamp | $shortCwd$gitBranch | $modelName" -NoNewline
