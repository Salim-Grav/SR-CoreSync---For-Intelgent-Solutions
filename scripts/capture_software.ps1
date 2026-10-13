$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$outImg1 = "C:\Users\msali\.gemini\antigravity-ide\brain\b4adc775-45bf-4bfa-8d40-6a12a92a104c\live_software_marketplace_upgraded.png"
$url = "http://localhost:3000/index.html#software-hub"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,1100",
    "--virtual-time-budget=3000",
    "--screenshot=$outImg1",
    $url
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Software screenshot saved: $outImg1"
