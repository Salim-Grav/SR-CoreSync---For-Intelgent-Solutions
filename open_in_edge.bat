@echo off
title "S&R CoreSync Solutions - Local Server & Edge"
chcp 65001 >nul
cd /d "%~dp0"

echo ======================================================================
echo   S^&R CoreSync Solutions - تشغيل السيرفر المحلي والمنفذ في Edge
echo ======================================================================
echo.

:: 1. فحص ما إذا كان السيرفر على المنفذ 3000 يعمل بالفعل
powershell -NoProfile -Command "$conn = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue; if ($conn) { exit 0 } else { exit 1 }"
if %errorlevel% equ 0 (
    echo [✓] السيرفر المحلي يعمل مسبقاً على: http://localhost:3000
    echo [✓] جاري فتح الموقع في Microsoft Edge مباشرة...
    start msedge http://localhost:3000/index.html
    ping 127.0.0.1 -n 3 >nul
    exit /b 0
)

:: 2. تشغيل السيرفر في الخلفية إذا لم يكن قيد التشغيل
echo [1] جاري تشغيل السيرفر المحلي على المنفذ: http://localhost:3000 ...

where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] تشغيل السيرفر عبر Python...
    start /b python serve.py >nul 2>&1
) else (
    echo [✓] تشغيل السيرفر عبر PowerShell...
    start /b powershell -NoProfile -ExecutionPolicy Bypass -Command "$port = 3000; $listener = New-Object System.Net.HttpListener; $listener.Prefixes.Add('http://localhost:' + $port + '/'); try { $listener.Start(); while ($listener.IsListening) { $ctx = $listener.GetContext(); $p = $ctx.Request.Url.LocalPath.TrimStart('/'); if ([string]::IsNullOrEmpty($p)) { $p = 'index.html' }; $f = Join-Path (Get-Location).Path $p; if (Test-Path $f -PathType Leaf) { $b = [System.IO.File]::ReadAllBytes($f); $ext = [System.IO.Path]::GetExtension($f).ToLower(); $m = switch ($ext) { '.html' {'text/html; charset=utf-8'} '.css' {'text/css'} '.js' {'application/javascript'} '.json' {'application/json'} '.svg' {'image/svg+xml'} default {'application/octet-stream'} }; $ctx.Response.ContentType = $m; $ctx.Response.ContentLength64 = $b.Length; $ctx.Response.OutputStream.Write($b, 0, $b.Length) } else { $ctx.Response.StatusCode = 404 }; $ctx.Response.OutputStream.Close() } } catch {}" >nul 2>&1
)

:: مهلة ثانية للاستعداد
ping 127.0.0.1 -n 2 >nul

:: 3. فتح الموقع في Edge
echo [2] فتح الموقع في Microsoft Edge...
start msedge http://localhost:3000/index.html
echo.
echo [✓] تم تشغيل الموقع والسيرفر بنجاح!
ping 127.0.0.1 -n 3 >nul
