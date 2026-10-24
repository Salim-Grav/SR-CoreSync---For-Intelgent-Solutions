$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$outImg = "C:\Users\msali\.gemini\antigravity-ide\brain\870f9005-7625-4bb2-a914-9e68dac4aa54\floating_hub_resolved.png"
$url = "http://localhost:3000/index.html"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,900",
    "--screenshot=$outImg",
    $url
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Screenshot done: $outImg"
