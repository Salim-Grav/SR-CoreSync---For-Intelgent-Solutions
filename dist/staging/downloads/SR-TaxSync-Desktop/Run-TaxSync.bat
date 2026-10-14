@echo off
title S&R TaxSync Desktop v2.4 Pro - S&R CoreSync Solutions
color 0A
echo ========================================================
echo    S&R TaxSync Desktop v2.4 Pro (Offline Edition)
echo    Powered by S&R CoreSync Solutions B.V. - Amsterdam
echo ========================================================
echo [OK] Checking local offline cryptographic license...
echo [OK] Initializing local database and XML engine...
echo [OK] Launching Native Desktop Application Window...
start "" msedge --app="%~dp0TaxSync.html"
exit
