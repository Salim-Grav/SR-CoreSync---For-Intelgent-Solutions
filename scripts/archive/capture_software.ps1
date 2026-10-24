$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$outImg2 = "C:\Users\msali\.gemini\antigravity-ide\brain\b4adc775-45bf-4bfa-8d40-6a12a92a104c\live_software_modal_download.png"
$url = "http://127.0.0.1:3000/preview-software-modal.html"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1400,980",
    "--screenshot=$outImg2",
    $url
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Software modal screenshot saved: $outImg2"
