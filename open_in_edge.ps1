# S&R CoreSync Solutions - Microsoft Edge Launcher
$port = 3000
$url = "http://localhost:$port/index.html"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   S&R CoreSync Solutions - تشغيل السيرفر المحلي والمنصة في Edge" -ForegroundColor Yellow
Write-Host "   Enterprise Cloud and Financial ERP Systems - Amsterdam HQ" -ForegroundColor DarkGray
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. فحص ما إذا كان السيرفر على المنفذ 3000 يعمل بالفعل
$conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($conn) {
    Write-Host "[✓] السيرفر المحلي يعمل مسبقاً على: $url" -ForegroundColor Green
    Write-Host "[✓] فتح متصفح Microsoft Edge مباشرة..." -ForegroundColor Green
    Start-Process msedge $url
    Start-Sleep -Seconds 2
    exit 0
}

# 2. تشغيل السيرفر في الخلفية
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "[i] جاري تشغيل سيرفر بايثون المحلي في الخلفية..." -ForegroundColor Cyan
    Start-Process python -ArgumentList 'serve.py' -WindowStyle Hidden
    Start-Sleep -Milliseconds 700
}

Write-Host "[✓] تم تشغيل المنصة بنجاح على: $url" -ForegroundColor Green
Write-Host "[✓] جاري فتح الموقع في Microsoft Edge..." -ForegroundColor Green
Start-Process msedge $url
Start-Sleep -Seconds 2
