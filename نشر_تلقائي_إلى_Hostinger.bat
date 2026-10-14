@echo off
chcp 65001 >nul
title S&R CoreSync Solutions — نشر تلقائي إلى Hostinger
color 0B
echo.
echo ===================================================================
echo  S^&R CoreSync Solutions — نشر تلقائي إلى Hostinger بنقرة زر واحدة
echo  Enterprise Cloud ^& Financial ERP Systems • Amsterdam HQ
echo ===================================================================
echo.
echo [1] محاكاة وتدقيق النشر (Dry-Run / Simulation)
echo [2] بناء وتحديث حزمة الإنتاج فقط (Production ZIP Package)
echo [3] تنفيذ النشر المباشر إلى السيرفر (Live Deployment via SSH/SFTP)
echo.
set /p choice="اختر رقم العملية (1 أو 2 أو 3) [الافتراضي: 1]: "

if "%choice%"=="2" (
    node scripts/deploy_hostinger.js --package-only
) else if "%choice%"=="3" (
    node scripts/deploy_hostinger.js
) else (
    node scripts/deploy_hostinger.js --dry-run
)

echo.
echo اضغط أي مفتاح للإغلاق...
pause >nul
