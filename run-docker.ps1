$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker is not installed/on PATH. Start Docker Desktop first.' }
docker compose up --build
