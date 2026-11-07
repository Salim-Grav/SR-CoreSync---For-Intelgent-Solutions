@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title SR-CoreSync - Automatic Updater (no questions)

REM =====================================================================
REM   SR-CoreSync - Automatic Updater
REM   NO QUESTIONS ASKED - just double-click and watch.
REM   Keep this file in the SAME folder as the two ZIP files.
REM =====================================================================

set "REPO_URL=https://github.com/Salim-Grav/SR-CoreSync---For-Intelgent-Solutions.git"
set "UPLOAD_PAGE=https://github.com/Salim-Grav/SR-CoreSync---For-Intelgent-Solutions/upload/main"
set "HERE=%~dp0"

echo =====================================================
echo   SR-CoreSync Automatic Updater
echo   (does everything for you - no questions asked)
echo =====================================================
echo.

REM ---------- 1) extract packages if needed ----------
if not exist "%HERE%SR-CoreSync_P0_Patches" if exist "%HERE%SR-CoreSync_P0_Patches.zip" (
    echo [1/6] Extracting security patches ...
    powershell -NoProfile -Command "Expand-Archive -LiteralPath '%HERE%SR-CoreSync_P0_Patches.zip' -DestinationPath '%HERE%' -Force"
)
if not exist "%HERE%SR-CoreSync_i18n_Fixes" if exist "%HERE%SR-CoreSync_i18n_Fixes.zip" (
    echo [1/6] Extracting translation fixes ...
    powershell -NoProfile -Command "Expand-Archive -LiteralPath '%HERE%SR-CoreSync_i18n_Fixes.zip' -DestinationPath '%HERE%' -Force"
)
if not exist "%HERE%SR-CoreSync_P0_Patches" (
    echo [ERROR] Cannot find SR-CoreSync_P0_Patches.
    echo         Put this file next to the two ZIP files and run again.
    pause
    exit /b 1
)
if not exist "%HERE%SR-CoreSync_i18n_Fixes" (
    echo [ERROR] Cannot find SR-CoreSync_i18n_Fixes.
    echo         Put this file next to the two ZIP files and run again.
    pause
    exit /b 1
)
echo       [OK] Both packages ready.
echo.

REM ---------- 2) check if git is available ----------
where git >nul 2>nul
if errorlevel 1 (
    echo [2/6] git not found - will use the easy browser method.
    echo.
    goto :browser_method
)
echo [2/6] git found.
echo.

REM ---------- 3) download a fresh copy from GitHub ----------
set "TARGET=%HERE%SR-CoreSync-project"
if exist "!TARGET!\.git" (
    echo [3/6] Updating the local copy I downloaded before ...
    cd /d "!TARGET!"
    git pull --quiet --no-rebase 2>nul
    cd /d "%HERE%"
) else (
    echo [3/6] Downloading your project from GitHub ...
    git clone --quiet "%REPO_URL%" "!TARGET!"
    if errorlevel 1 (
        echo       [ERROR] Download failed. Check your internet connection.
        echo       Falling back to easy browser method ...
        echo.
        goto :browser_method
    )
)
echo       [OK] Project ready at: !TARGET!
echo.

REM ---------- 4) apply both packages ----------
echo [4/6] Applying security patches (P0) ...
xcopy /E /I /Y /Q "%HERE%SR-CoreSync_P0_Patches\full_files" "!TARGET!" >nul
echo [4/6] Applying translation fixes (all 26 languages) ...
xcopy /E /I /Y /Q "%HERE%SR-CoreSync_i18n_Fixes\full_files" "!TARGET!" >nul
echo       [OK] All files are in place.
echo.

REM ---------- 5) commit ----------
cd /d "!TARGET!"
git add -A
git commit -m "Apply SR-CoreSync updates: P0 security patches + full i18n translation fixes" 2>nul
echo [5/6] Changes saved locally.
echo.

REM ---------- 6) push to GitHub ----------
echo [6/6] Sending to GitHub ...
echo       A browser window may open asking you to log in.
echo       Give your approval there - nothing is sent without it.
echo.
git push
if errorlevel 1 (
    echo.
    echo [NOTE] Auto-push did not finish (maybe GitHub login needed).
    echo        Falling back to easy browser method ...
    echo.
    goto :browser_method
)
echo.
echo       [OK] GitHub is now up to date! Refresh the page to see it.
echo.
echo =====================================================
echo   All done. You can close this window.
echo =====================================================
pause
exit /b 0

:browser_method
echo [browser] Preparing files for easy drag-and-drop upload ...
mkdir "%HERE%GITHUB_UPLOAD" 2>nul
xcopy /E /I /Y /Q "%HERE%SR-CoreSync_P0_Patches\full_files" "%HERE%GITHUB_UPLOAD" >nul
xcopy /E /I /Y /Q "%HERE%SR-CoreSync_i18n_Fixes\full_files" "%HERE%GITHUB_UPLOAD" >nul
echo          [OK] Folder ready.
echo.
echo =====================================================
echo   LAST STEP - 3 simple actions:
echo.
echo   1. A browser page opened: GitHub Upload files.
echo   2. A folder opened: GITHUB_UPLOAD
echo      Drag EVERYTHING from that folder into the browser.
echo   3. Click "Commit changes" at the bottom. Done!
echo =====================================================
echo.
start "" "%UPLOAD_PAGE%"
timeout /t 2 >nul
start "" explorer "%HERE%GITHUB_UPLOAD"
pause
exit /b 0
