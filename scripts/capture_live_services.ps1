$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$outImg = "C:\Users\msali\.gemini\antigravity-ide\brain\b4adc775-45bf-4bfa-8d40-6a12a92a104c\live_services_clean_preview.png"
$url = "http://127.0.0.1:3000/preview-services.html"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,1100",
    "--screenshot=$outImg",
    $url
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

if (Test-Path $outImg) {
    Write-Host "SNAPSHOT_SUCCESS: $outImg"
} else {
    Write-Host "SNAPSHOT_FAILED"
}
