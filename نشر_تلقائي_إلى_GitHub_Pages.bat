@echo off
chcp 65001 >nul
title S&R CoreSync Solutions — نشر تلقائي إلى GitHub Pages
color 0b

echo.
echo  =======================================================================
echo   S^&R CoreSync Solutions — نشر تلقائي إلى GitHub Pages بنقرة زر واحدة
echo   Enterprise Cloud ^& Financial ERP Systems • Amsterdam HQ
echo  =======================================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\deploy.ps1"

echo.
pause
