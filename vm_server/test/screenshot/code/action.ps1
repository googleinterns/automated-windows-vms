$scriptpath = $MyInvocation.MyCommand.Path
Write-Host $scriptpath
python .\code\execute.py
Write-Host "Execution Done"