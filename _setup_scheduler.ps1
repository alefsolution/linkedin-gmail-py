# set-executionpolicy remotesigned
$dirname = pwd | Select-Object | %{$_.ProviderPath.Split("\")[-1]} 
$taskname = "Linkedin " + $dirname
$user = 'Administrator'

[int]$choice = Read-Host "Select password 1), 2)"
$pwd = switch ($choice) {
  1 { '' }
  2 { '' }
}

$repeat = (New-TimeSpan -Minutes 20)

$script_dir = pwd | Select-Object | %{$_.ProviderPath}
$updater = $script_dir + "\_update_and_run.bat"
$chdir = "cd " + $script_dir

New-Item $updater -ItemType File -Value ($chdir + [Environment]::NewLine)
Add-Content $updater ("git pull")
Add-Content $updater ("python bot.py")

$Action =  New-ScheduledTaskAction -Execute $updater
$Trigger = New-JobTrigger -Once -At (Get-Date) -RepeatIndefinitely -RepetitionInterval $repeat
$Settings = New-ScheduledTaskSettingsSet
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings
Register-ScheduledTask -TaskName $taskname -InputObject $Task -User $user -Password $pwd
