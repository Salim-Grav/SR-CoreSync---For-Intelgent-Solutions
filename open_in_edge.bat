@echo off
chcp 65001 >nul
title "S&R CoreSync Solutions — تشغيل الموقع في Edge"
color 0A
cd /d "%~dp0"

echo.
echo ======================================================================
echo   S^&R CoreSync Solutions - تشغيل السيرفر المحلي والمنصة في Edge
echo   Enterprise Cloud ^& Financial ERP Systems • Amsterdam HQ
echo ======================================================================
echo.
echo [1] فحص السيرفر المحلي على المنفذ 3000...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$port = 3000; $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue; if (-not $conn) { Write-Host '[i] جاري تشغيل سيرفر بايثون المحلي في الخلفية...' -ForegroundColor Cyan; Start-Process python -ArgumentList 'serve.py' -WindowStyle Hidden; Start-Sleep -Milliseconds 700 } else { Write-Host '[✓] السيرفر المحلي يعمل مسبقاً.' -ForegroundColor Green }; Write-Host '[✓] فتح متصفح Microsoft Edge على الرابط: http://localhost:3000/index.html' -ForegroundColor Green; Start-Process msedge 'http://localhost:3000/index.html'"

echo.
echo [✓] تم تشغيل المنصة بنجاح!
ping 127.0.0.1 -n 3 >nul
