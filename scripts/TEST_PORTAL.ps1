$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
py -3 -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Offline tests failed.' }
py -3 scripts/validate_catalog.py
if ($LASTEXITCODE -ne 0) { throw 'Public catalog invalid.' }
Write-Host 'OFFLINE GATES PASS; Windows Edge/Chrome and hosting security remain to be validated.' -ForegroundColor Green
