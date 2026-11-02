@echo off
setlocal enabledelayedexpansion
title SR-CoreSync - Automatic Updater

REM =====================================================================
REM   SR-CoreSync - Automatic Updater (does everything on your behalf)
REM   Put this file in the SAME folder as the two ZIP files, then run it.
REM =====================================================================

set "REPO_URL=https://github.com/Salim-Grav/SR-CoreSync---For-Intelgent-Solutions.git"
set "UPLOAD_PAGE=https://github.com/Salim-Grav/SR-CoreSync---For-Intelgent-Solutions/upload/main"
set "HERE=%~dp0"

echo =====================================================
echo   SR-CoreSync Automatic Updater
echo   (updates your project + GitHub with one approval)
echo =====================================================
echo.

REM ---------- 1) make sure both packages are available ----------
if not exist "%HERE%SR-CoreSync_P0_Patches" if exist "%HERE%SR-CoreSync_P0_Patches.zip" (
    echo [prepare] Extracting SR-CoreSync_P0_Patches.zip ...
    powershell -NoProfile -Command "Expand-Archive -LiteralPath '%HERE%SR-CoreSync_P0_Patches.zip' -DestinationPath '%HERE%' -Force"
)
if not exist "%HERE%SR-CoreSync_i18n_Fixes" if exist "%HERE%SR-CoreSync_i18n_Fixes.zip" (
    echo [prepare] Extracting SR-CoreSync_i18n_Fixes.zip ...
    powershell -NoProfile -Command "Expand-Archive -LiteralPath '%HERE%SR-CoreSync_i18n_Fixes.zip' -DestinationPath '%HERE%' -Force"
)
if not exist "%HERE%SR-CoreSync_P0_Patches" (
    echo [ERROR] I could not find the packages.
    echo         Keep this file in the same folder as the two ZIP files.
    pause
    exit /b 1
)
if not exist "%HERE%SR-CoreSync_i18n_Fixes" (
    echo [ERROR] The translation package is missing next to this file.
    pause
    exit /b 1
)
echo [prepare] Both packages found and ready.
echo.

REM ---------- 2) decide WHERE to apply ----------
echo Where is your project?
echo   - Drag your existing project folder into this window and press Enter,
echo   - or just press ENTER to download a fresh copy from GitHub.
set /p "TARGET=> "
set "TARGET=!TARGET:"=!"
set "TARGET=!TARGET:/=!"
if "!TARGET!"=="" (
    where git >nul 2>nul
    if errorlevel 1 (
        echo.
        echo [INFO] git is not installed, so I cannot download or push
        echo        automatically. I will prepare a ready upload folder for
        echo        the browser method instead - very easy, 3 clicks.
        set "GIT_MISSING=1"
        set "TARGET=%HERE%updated-project"
    ) else (
        set "TARGET=%HERE%SR-CoreSync-project"
        if not exist "!TARGET!" (
            echo [download] Downloading your project from GitHub ...
            git clone --quiet "%REPO_URL%" "!TARGET!"
            if errorlevel 1 (
                echo [ERROR] Download failed. Check your internet connection.
                pause
                exit /b 1
            )
        )
    )
)
if not exist "!TARGET!" (
    echo [ERROR] Folder not found: !TARGET!
    pause
    exit /b 1
)
echo [target] !TARGET!
echo.

REM ---------- 3) apply both packages ----------
echo [apply 1/2] Copying security update files - P0 ...
xcopy /E /I /Y "%HERE%SR-CoreSync_P0_Patches\full_files" "!TARGET!" >nul
echo [apply 2/2] Copying translation files - all languages ...
xcopy /E /I /Y "%HERE%SR-CoreSync_i18n_Fixes\full_files" "!TARGET!" >nul
echo             [OK] All files are in place.
echo.

REM ---------- 4) send to GitHub ----------
if defined GIT_MISSING (
    mkdir "%HERE%GITHUB_UPLOAD" 2>nul
    xcopy /E /I /Y "%HERE%SR-CoreSync_P0_Patches\full_files" "%HERE%GITHUB_UPLOAD" >nul
    xcopy /E /I /Y "%HERE%SR-CoreSync_i18n_Fixes\full_files" "%HERE%GITHUB_UPLOAD" >nul
    echo =====================================================
    echo   LAST STEP - 3 clicks, I opened the page for you:
    echo   1. A browser page opened: Upload files on GitHub.
    echo   2. Drag EVERYTHING you see inside the folder
      echo      GITHUB_UPLOAD into that page.
    echo   3. Click Commit changes. Done!
    echo =====================================================
    start "" "%UPLOAD_PAGE%"
    start "" explorer "%HERE%GITHUB_UPLOAD"
    pause
    exit /b 0
)

if exist "!TARGET!\.git" (
    cd /d "!TARGET!"
    echo [github] Saving changes...
    git add -A
    git commit -m "Apply SR-CoreSync updates: P0 security patches + full i18n translation fixes"
    echo.
    echo [github] Sending to GitHub...
    echo          A browser window may open asking you to log in.
    echo          Give your approval there - nothing is sent without it.
    echo.
    git push
    if errorlevel 1 (
        echo          [NOTE] Push did not finish - your copy may be behind
        echo                 GitHub. Run:  git pull   then   git push
    ) else (
        echo          [OK] GitHub is now up to date! Refresh the page to see it.
    )
) else (
    echo [github] This folder has no git repository, so nothing was sent.
    echo          Disk files were updated - enough if this is your live folder.
)

echo.
echo =====================================================
echo   All done. You can close this window.
echo =====================================================
echo.
pause
