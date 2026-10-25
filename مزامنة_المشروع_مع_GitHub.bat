@echo off
chcp 65001 > nul
title مزامنة مشروع S&R CoreSync مع GitHub
color 0b

cd /d "d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project"

:menu
cls
echo ======================================================================
echo          S&R CoreSync - أداة المزامنة السريعة مع GitHub
echo ======================================================================
echo.
echo  [1] سحب التحديثات من GitHub (Pull) - عند العودة من ZaiChat
echo  [2] حفظ ودفع التحديثات إلى GitHub (Push) - قبل الانتقال إلى ZaiChat
echo  [3] مزامنة ذكية كاملة (Pull ثم فحص الحالة)
echo  [4] فحص حالة المستودع (Git Status)
echo  [5] خروج
echo.
echo ======================================================================
set /p choice="اختر رقم العملية (1-5) ثم اضغط Enter: "

if "%choice%"=="1" goto pull_code
if "%choice%"=="2" goto push_code
if "%choice%"=="3" goto smart_sync
if "%choice%"=="4" goto check_status
if "%choice%"=="5" exit
goto menu

:pull_code
echo.
echo 📥 جاري سحب أحدث التعديلات من GitHub...
git pull origin main
echo.
echo ✅ اكتمل فحص وسحب التحديثات بنجاح.
echo.
pause
goto menu

:push_code
echo.
set /p commit_msg="اكتب وصف التحديث (أو اضغط Enter للاعتماد التلقائي): "
if "%commit_msg%"=="" set commit_msg="feat: sync updates between IDEs"
echo.
echo 📤 جاري تجهيز الملفات وحفظ الالتزام...
git add -A
git commit -m %commit_msg%
echo 🚀 جاري الرفع المباشر إلى GitHub...
git push origin main
echo.
echo ✅ تم دفع كافة التحديثات إلى GitHub بنجاح!
echo.
pause
goto menu

:smart_sync
echo.
echo 🔄 جاري التحقق وسحب التحديثات...
git pull origin main
echo.
echo 📊 ملخص الملفات الحالية:
git status -s
echo.
pause
goto menu

:check_status
echo.
echo 📊 فحص حالة شجرة العمل:
git status
echo.
pause
goto menu
