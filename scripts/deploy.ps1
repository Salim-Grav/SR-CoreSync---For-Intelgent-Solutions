<#
.SYNOPSIS
    S&R CoreSync Solutions — سكربت النشر التلقائي المعتمد لخوادم Hostinger
    Enterprise Cloud & Financial ERP Systems • Amsterdam HQ

.DESCRIPTION
    يقوم هذا السكربت بالتدقيق الآلي، حزم ملفات الإنتاج المعتمدة،
    ورفعها وفك ضغطها تلقائياً على خوادم Hostinger cPanel / hPanel بنقرة واحدة.

.EXAMPLE
    .\scripts\deploy.ps1 -DryRun
    .\scripts\deploy.ps1 -Deploy
#>

[CmdletBinding()]
param (
    [switch]$DryRun,
    [switch]$PackageOnly,
    [switch]$Force
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "S&R CoreSync — Hostinger Automated Deployer"

Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host " 🚀 S&R CoreSync Solutions — محرك النشر التلقائي لخوادم Hostinger" -ForegroundColor Yellow
Write-Host " Enterprise Cloud & Financial ERP Systems • Amsterdam HQ" -ForegroundColor Gray
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectPath = Split-Path -Parent $ScriptPath

Set-Location $ProjectPath

$NodeArgs = @("scripts/deploy_hostinger.js")

if ($DryRun) {
    $NodeArgs += "--dry-run"
}
if ($PackageOnly) {
    $NodeArgs += "--package-only"
}
if ($Force) {
    $NodeArgs += "--force"
}

Write-Host "جارٍ تشغيل محرك النشر التلقائي عبر Node.js..." -ForegroundColor DarkYellow
node @NodeArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✔ تمت المهمة بنجاح كامل!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✖ حدث خطأ أثناء تشغيل محرك النشر." -ForegroundColor Red
}
