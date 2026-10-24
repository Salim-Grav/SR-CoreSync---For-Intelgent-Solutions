$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}
$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$outImg1 = "C:\Users\msali\.gemini\antigravity-ide\brain\0fa97aaa-2c0d-46de-bd13-ab949ab18753\slider_showcase_salim.png"
$outImg2 = "C:\Users\msali\.gemini\antigravity-ide\brain\0fa97aaa-2c0d-46de-bd13-ab949ab18753\slider_showcase_raed.png"

# 1. Capture Slide 0 (Salim)
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,1180",
    "--screenshot=$outImg1",
    "http://localhost:3000/preview-founders-showcase.html?slide=0"
) -Wait

Start-Sleep -Seconds 1

# 2. Capture Slide 1 (Raed)
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,1180",
    "--screenshot=$outImg2",
    "http://localhost:3000/preview-founders-showcase.html?slide=1"
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Captured both slides successfully!"
