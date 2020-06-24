$scriptpath = $MyInvocation.MyCommand.Path
Write-host $scriptpath
python .\code\execute.py
Write-Host "Execution Done"