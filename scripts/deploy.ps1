<#
.SYNOPSIS
    S&R CoreSync Solutions — سكربت النشر التلقائي المعتمد لمنصة GitHub Pages
    Enterprise Cloud & Financial ERP Systems • Amsterdam HQ

.DESCRIPTION
    يقوم هذا السكربت بالتحقق الآلي من الحزمة، تجهيز حزمة النشر _site/،
    والتأكد من عدم وجود أي ملفات سرية أو خاصة بالخادم، ثم الدفع المباشر
    إلى فرع main على GitHub لإطلاق سير العمل التلقائي (GitHub Actions).

.EXAMPLE
    .\scripts\deploy.ps1
    .\scripts\deploy.ps1 -BuildOnly
#>

[CmdletBinding()]
param (
    [switch]$BuildOnly,
    [string]$CommitMessage = "deploy: sync production assets to GitHub Pages"
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "S&R CoreSync — GitHub Pages Automated Deployer"

Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host " 🚀 S&R CoreSync Solutions — محرك النشر التلقائي لـ GitHub Pages" -ForegroundColor Yellow
Write-Host " Enterprise Cloud & Financial ERP Systems • Amsterdam HQ" -ForegroundColor Gray
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectPath = Split-Path -Parent $ScriptPath
Set-Location $ProjectPath

# 1. تشغيل بناء حزمة النشر
Write-Host "[1/3] جاري تجهيز والتحقق من حزمة النشر _site/..." -ForegroundColor Cyan
python scripts\prepare_publish_set.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "✖ فشل التحقق من حزمة النشر. يرجى مراجعة الأخطاء أعلاه." -ForegroundColor Red
    exit 1
}

if ($BuildOnly) {
    Write-Host ""
    Write-Host "✔ تم تجهيز حزمة _site/ بنجاح دون النشر." -ForegroundColor Green
    exit 0
}

# 2. فحص حالة Git
Write-Host ""
Write-Host "[2/3] فحص التغييرات وتجهيز الالتزام..." -ForegroundColor Cyan
git status -s

# 3. دفع التغييرات إلى المستودع العام
Write-Host ""
Write-Host "[3/3] مزامنة ودفع التحديثات إلى GitHub Pages (main branch)..." -ForegroundColor Cyan
git add .
$status = git status --porcelain
if ($status) {
    git commit -m "$CommitMessage"
}

git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "===================================================================" -ForegroundColor Green
    Write-Host " ✔ تم النشر بنجاح إلى GitHub Pages!" -ForegroundColor Green
    Write-Host " تم إطلاق سير العمل التلقائي على GitHub Actions بنجاح." -ForegroundColor Green
    Write-Host " الموقع الحي: https://sr-coresync.com/ (أو رابط صفحات GitHub)" -ForegroundColor Yellow
    Write-Host "===================================================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✖ حدث خطأ أثناء الدفع إلى GitHub." -ForegroundColor Red
}
