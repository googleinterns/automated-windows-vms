$scriptpath = $MyInvocation.MyCommand.Path
Write-host $scriptpath
python .\code\execute.py
if ( $LASTEXITCODE -ne 0 ) { 
   Write-Warning "Exiting with code $LASTEXITCODE" 
   exit $LASTEXITCODE
}