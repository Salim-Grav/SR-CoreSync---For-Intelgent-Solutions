@echo off
title S&R CoreSync Solutions - Founders Showcase Launcher
chcp 65001 >nul
cd /d "%~dp0"

echo ==============================================================================
echo       S&R CORESYNC SOLUTIONS - تشغيل معاينة بانرات القيادة التنفيذية
echo ==============================================================================
echo.
echo [1] فحص السيرفر المحلي على المنفذ: http://localhost:3000 ...

powershell -NoProfile -Command "$conn = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue; if (-not $conn) { Start-Process python -ArgumentList 'serve.py' -WindowStyle Hidden; Start-Sleep -Milliseconds 800 }"

echo [2] فتح صفحة المعاينة التفاعلية في Microsoft Edge...
start msedge http://localhost:3000/preview-founders-showcase.html
echo.
echo [✓] تم فتح المعاينة بنجاح!
timeout /t 3 >nul
