$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

$serverJob = Start-Process python -ArgumentList @("-m", "http.server", "8000") -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 2

$url = "http://localhost:8000/preview-license-manager.html"
$outImg = "C:\Users\msali\.gemini\antigravity-ide\brain\c343b500-bda0-4fad-aa48-4c2182879e6c\live_executive_license_ledger.png"

# We open Edge and capture with larger height to cover full dashboard and table
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,1650",
    "--screenshot=$outImg",
    $url
) -Wait

Start-Sleep -Seconds 1
Stop-Process -Id $serverJob.Id -Force -ErrorAction SilentlyContinue
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Ledger Snapshot captured: $outImg"
