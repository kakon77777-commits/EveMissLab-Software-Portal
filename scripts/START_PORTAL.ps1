$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
py -3 scripts/validate_catalog.py
if ($LASTEXITCODE -ne 0) { throw 'Public catalog failed validation.' }
Write-Host 'Open http://127.0.0.1:8080' -ForegroundColor Cyan
py -3 -m http.server 8080 --bind 127.0.0.1
