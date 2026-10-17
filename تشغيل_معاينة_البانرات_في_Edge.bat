@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$port = 3000; $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue; if (-not $conn) { Start-Process python -ArgumentList 'serve.py' -WindowStyle Hidden; Start-Sleep -Milliseconds 600 }; Start-Process msedge ('http://localhost:' + $port + '/preview-founders-showcase.html')"
