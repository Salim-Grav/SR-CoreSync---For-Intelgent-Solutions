@echo off
setlocal enabledelayedexpansion
title SR-CoreSync Update Applier

echo ==================================================
echo    SR-CoreSync - Apply Updates (one click)
echo ==================================================
echo.
echo This tool copies the updated files from "full_files"
echo into your project folder, and if that folder is a git
echo repository it also commits and pushes them to GitHub.
echo.

set "SRC=%~dp0full_files"
if not exist "%SRC%" (
    echo [ERROR] "full_files" folder was not found next to this script.
    echo         Keep this script inside the extracted package folder.
    pause
    exit /b 1
)

if "%~1"=="" (
    echo Drag your project folder into this window, then press Enter:
    set /p "REPO=> "
) else (
    set "REPO=%~1"
)
set "REPO=!REPO:"=!"
if "!REPO!"=="" (
    echo [ERROR] No folder was given.
    pause
    exit /b 1
)
if not exist "!REPO!" (
    echo [ERROR] Project folder not found: !REPO!
    pause
    exit /b 1
)

echo.
echo [1/2] Copying updated files into: !REPO!
echo.

for %%F in ("%SRC%\*") do (
    copy /Y "%%F" "!REPO!\%%~nxF" >nul
)
for /D %%D in ("%SRC%\*") do (
    xcopy /E /I /Y "%%D" "!REPO!\%%~nxD" >nul
)
echo       [OK] All files copied. Existing files with the same
echo            names were overwritten - this is expected.
echo.

if exist "!REPO!\.git" (
    echo [2/2] Git repository detected. Saving changes...
    cd /d "!REPO!"
    git add -A
    git commit -m "Apply SR-CoreSync updates: P0 security patches + full i18n translation fixes"
    echo.
    echo       Now pushing to GitHub...
    echo       A browser window may open asking you to log in.
    echo       >>> Approve it there - nothing uploads without your OK. <<<
    echo.
    git push
    if errorlevel 1 (
        echo       [NOTE] Push did not finish - your copy may be behind
        echo              GitHub. Run:  git pull   then   git push
    ) else (
        echo       [OK] Successfully pushed to GitHub!
    )
) else (
    echo [2/2] No .git folder found here, so nothing was sent to
    echo       GitHub. Disk files were updated - that is all you need
    echo       if this copy is your live website folder.
)

echo.
echo ==================================================
echo    Done. You can close this window.
echo ==================================================
echo.
pause
