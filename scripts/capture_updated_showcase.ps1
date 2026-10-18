$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\6c3789a5-12b8-47a7-ae30-f1a347854cd7"
$outSlide0 = Join-Path $artDir "live_showcase_slide0_emblem.png"
$outSlide2 = Join-Path $artDir "live_showcase_slide2_raed.png"

# 1. Capture Slide 0 (Emblem)
$tempDir0 = Join-Path $env:TEMP ("edge_cap0_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir0",
    "--window-size=1440,1200",
    "--screenshot=$outSlide0",
    "http://localhost:3000/index.html#founders-showcase"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDir0 -Recurse -Force -ErrorAction SilentlyContinue

# 2. Capture Slide 2 (Raed with new emblem) by opening viewRaed
$outRaedView = Join-Path $artDir "live_showcase_raed_view.png"
$tempDir2 = Join-Path $env:TEMP ("edge_cap2_" + [Guid]::NewGuid().ToString())
# We can open preview-founders-showcase with ?view=raed or an injected script
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir2",
    "--window-size=1440,1200",
    "--screenshot=$outRaedView",
    "http://localhost:3000/preview-founders-showcase.html?view=raed"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDir2 -Recurse -Force -ErrorAction SilentlyContinue

# 3. Capture Dual / Full Showcase
$outFull = Join-Path $artDir "live_showcase_full_grid.png"
$tempDir3 = Join-Path $env:TEMP ("edge_cap3_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir3",
    "--window-size=1440,1600",
    "--screenshot=$outFull",
    "http://localhost:3000/preview-founders-showcase.html?view=dual"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDir3 -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Slide 0: $(Test-Path $outSlide0)"
Write-Host "Raed View: $(Test-Path $outRaedView)"
Write-Host "Full Grid: $(Test-Path $outFull)"
