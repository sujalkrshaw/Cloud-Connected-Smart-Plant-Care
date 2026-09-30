# 10-Minute Quickstart

## Recommended if Docker Desktop is working

```powershell
cd "C:\path\to\Cloud-Connected-Smart-Plant-Care"
.\run-docker.ps1
```

Then open:

- Dashboard: http://localhost:8080
- API docs: http://localhost:8000/docs

The simulator is already part of the Docker Compose stack.

## If you do not want Docker

```powershell
.\setup-local.ps1
```

This creates a Python virtual environment, installs backend packages, installs frontend packages, starts backend/frontend/simulator terminals, and opens the dashboard.

## Expected demonstration

Start around 55% moisture -> moisture gradually falls -> below 40% -> automatic watering starts -> virtual pump is ON -> moisture rises -> pump stops -> watering event and alert/history appear.

## If PowerShell blocks scripts

Run PowerShell as your normal user and use:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Then run the script again.
