$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}
$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$outImg = "C:\Users\msali\.gemini\antigravity-ide\brain\0fa97aaa-2c0d-46de-bd13-ab949ab18753\slider_showcase_full_view.png"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,1350",
    "--screenshot=$outImg",
    "http://localhost:3000/preview-founders-showcase.html?slide=0"
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Captured full view successfully!"
