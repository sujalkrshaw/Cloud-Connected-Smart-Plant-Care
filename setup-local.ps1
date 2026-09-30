$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
Write-Host "=== Smart Plant Cloud - local setup ===" -ForegroundColor Green
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python is not installed or not on PATH.' }
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw 'Node.js/npm is not installed or not on PATH.' }
if (-not (Test-Path '.venv')) { python -m venv .venv }
& "$Root\.venv\Scripts\python.exe" -m pip install -r "$Root\backend\requirements.txt"
Set-Location "$Root\frontend"
npm install
Set-Location $Root
Write-Host "Dependencies installed. Opening 3 development terminals..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList '-NoExit','-Command',"Set-Location '$Root\backend'; & '$Root\.venv\Scripts\Activate.ps1'; python -m uvicorn app.main:app --reload --port 8000"
Start-Process powershell -ArgumentList '-NoExit','-Command',"Set-Location '$Root\frontend'; npm run dev"
Start-Process powershell -ArgumentList '-NoExit','-Command',"Set-Location '$Root\sensor_simulator'; python simulator.py"
Start-Sleep -Seconds 3
Start-Process 'http://localhost:5173'
Write-Host 'Dashboard: http://localhost:5173' -ForegroundColor Green
Write-Host 'API docs:  http://localhost:8000/docs' -ForegroundColor Green
