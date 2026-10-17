# S&R CoreSync Solutions - Microsoft Edge Launcher
$port = 3000
$url = "http://localhost:$port/index.html"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  S`&R CoreSync Solutions - Enterprise Local Launcher" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# Check if port 3000 is already active
$conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($conn) {
    Write-Host "[OK] Local server is already running on port $port" -ForegroundColor Green
    Write-Host "[OK] Opening Microsoft Edge directly: $url" -ForegroundColor Green
    Start-Process msedge $url
    Start-Sleep -Seconds 2
    exit 0
}

# Start server if not running
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Starting local server via Python on $url..." -ForegroundColor Green
    Start-Process msedge $url
    python "$PSScriptRoot\serve.py"
} else {
    Write-Host "[OK] Opening Microsoft Edge directly..." -ForegroundColor Green
    Start-Process msedge $url
}
