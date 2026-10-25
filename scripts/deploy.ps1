# S&R CoreSync Solutions - Automated GitHub Pages Deployer
# Enterprise Cloud & Financial ERP Systems - Amsterdam HQ

param (
    [switch]$BuildOnly,
    [string]$CommitMessage = "deploy: sync production assets to GitHub Pages"
)

$ErrorActionPreference = "Stop"

try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
} catch {}

Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "  S&R CoreSync Solutions - GitHub Pages Deployer" -ForegroundColor Yellow
Write-Host "  Enterprise Cloud & Financial ERP Systems - Amsterdam HQ" -ForegroundColor Gray
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

# 1. Build & Verify publish set (_site)
Write-Host "[1/3] Preparing and verifying _site/ publish set..." -ForegroundColor Cyan
python scripts\prepare_publish_set.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[X] Publish set preparation failed." -ForegroundColor Red
    exit 1
}

if ($BuildOnly) {
    Write-Host ""
    Write-Host "[OK] _site/ staging completed successfully (BuildOnly mode)." -ForegroundColor Green
    exit 0
}

# 2. Check Git status
Write-Host ""
Write-Host "[2/3] Checking Git status..." -ForegroundColor Cyan
git status -s

# 3. Commit and push to GitHub
Write-Host ""
Write-Host "[3/3] Syncing and pushing updates to GitHub Pages (main branch)..." -ForegroundColor Cyan
git add .
$changes = git status --porcelain
if ($changes) {
    git commit -m "$CommitMessage"
}

git push origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "===================================================================" -ForegroundColor Green
    Write-Host " [OK] Successfully deployed to GitHub Pages!" -ForegroundColor Green
    Write-Host " GitHub Actions workflow triggered: .github/workflows/deploy-pages.yml" -ForegroundColor Green
    Write-Host " Live Site: https://sr-coresync.com/ or https://Salim-Grav.github.io/SR-CoreSync---For-Intelgent-Solutions/" -ForegroundColor Yellow
    Write-Host "===================================================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[X] Push failed. Check your network or GitHub credentials." -ForegroundColor Red
    exit 1
}
