' NAJIKA AUTO TRAINING - VBScript Version (minimiert im Hintergrund)
' Wartet bis 00:00 Uhr, startet dann Training automatisch

Set WshShell = CreateObject("WScript.Shell")

' Warte bis Mitternacht
Do While Hour(Now) <> 0
    ' Alle 5 Minuten prüfen
    WScript.Sleep 300000
Loop

' Mitternacht erreicht - Training starten!
' CMD minimiert im Hintergrund
WshShell.Run "cmd /c cd /d C:\Najika-World\backend && python najika_intensive_night_training.py && pause", 7, False

' Erfolgs-Nachricht
MsgBox "Najika Training gestartet! Log: backend\training_night_log.json", vbInformation, "Najika Training"
