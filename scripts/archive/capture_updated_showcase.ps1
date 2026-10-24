$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\6c3789a5-12b8-47a7-ae30-f1a347854cd7"
$outEmblem = Join-Path $artDir "live_showcase_slide0_emblem.png"
$outSalim = Join-Path $artDir "live_showcase_slide1_salim.png"
$outRaed = Join-Path $artDir "live_showcase_slide2_raed.png"
$outFull = Join-Path $artDir "live_showcase_full_grid.png"
$outSlider = Join-Path $artDir "live_showcase_slider_active.png"

# 1. Capture Emblem View
$tempDir0 = Join-Path $env:TEMP ("edge_cap0_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir0",
    "--window-size=1440,1100",
    "--screenshot=$outEmblem",
    "http://localhost:3000/preview-founders-showcase.html?view=emblem"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDir0 -Recurse -Force -ErrorAction SilentlyContinue

# 2. Capture Salim View
$tempDir1 = Join-Path $env:TEMP ("edge_cap1_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir1",
    "--window-size=1440,1100",
    "--screenshot=$outSalim",
    "http://localhost:3000/preview-founders-showcase.html?view=salim"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDir1 -Recurse -Force -ErrorAction SilentlyContinue

# 3. Capture Raed View (with new luxury orbital emblem)
$tempDir2 = Join-Path $env:TEMP ("edge_cap2_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir2",
    "--window-size=1440,1100",
    "--screenshot=$outRaed",
    "http://localhost:3000/preview-founders-showcase.html?view=raed"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDir2 -Recurse -Force -ErrorAction SilentlyContinue

# 4. Capture Full Grid View (All 3 Cards)
$tempDir3 = Join-Path $env:TEMP ("edge_cap3_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir3",
    "--window-size=1440,1500",
    "--screenshot=$outFull",
    "http://localhost:3000/preview-founders-showcase.html?view=dual"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDir3 -Recurse -Force -ErrorAction SilentlyContinue

# 5. Capture Slider Mode (Opening with Emblem Slide 0)
$tempDir4 = Join-Path $env:TEMP ("edge_cap4_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir4",
    "--window-size=1440,1150",
    "--screenshot=$outSlider",
    "http://localhost:3000/preview-founders-showcase.html?view=slider"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDir4 -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Emblem: $(Test-Path $outEmblem)"
Write-Host "Salim: $(Test-Path $outSalim)"
Write-Host "Raed: $(Test-Path $outRaed)"
Write-Host "Full: $(Test-Path $outFull)"
Write-Host "Slider: $(Test-Path $outSlider)"
