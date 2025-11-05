$WS = New-Object -ComObject WScript.Shell
$SC = $WS.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Najika World.lnk')
$SC.TargetPath = 'C:\Najika-World\START.bat'
$SC.WorkingDirectory = 'C:\Najika-World'
$SC.Save()
Write-Host "Desktop shortcut created!"
