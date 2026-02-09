# ═══════════════════════════════════════════════════════════════════════════
#  NAJIKA CODE - Lokale CLI wie Claude Code
#
#  Installation:
#    1. Füge diesen Ordner zum PATH hinzu, ODER
#    2. Kopiere najika.ps1 nach C:\Users\DEIN_NAME\Documents\WindowsPowerShell\
#    3. In PowerShell: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#
#  Nutzung:
#    najika              -> Interaktiver Modus
#    najika "Frage"      -> Einzel-Anfrage
#    najika --scan       -> Projekt scannen
#    najika --search X   -> Suche nach X
#    najika --todos      -> Alle TODOs finden
#    najika --treasures  -> Verlorene Schätze finden
# ═══════════════════════════════════════════════════════════════════════════

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Pfad zum Najika-Backend
$NajikaDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$NajikaScript = Join-Path $NajikaDir "backend\najika_code.py"

# Setze UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Starte Python
if ($Arguments) {
    python $NajikaScript $Arguments
} else {
    python $NajikaScript
}
