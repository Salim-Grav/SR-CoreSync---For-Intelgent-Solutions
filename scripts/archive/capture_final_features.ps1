$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\6c3789a5-12b8-47a7-ae30-f1a347854cd7"
$out1 = Join-Path $artDir "live_showcase_with_4k_qr.png"
$out2 = Join-Path $artDir "live_qr_modal_showcase.png"
$out3 = Join-Path $artDir "live_lightbox_4k_toolbar.png"

# 1. Slider card with full footer showing 4K & QR buttons (1440x1350)
$temp1 = Join-Path $env:TEMP ("edge_cap1_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp1",
    "--window-size=1440,1350",
    "--screenshot=$out1",
    "http://localhost:3000/preview-founders-showcase.html?view=slider"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp1 -Recurse -Force -ErrorAction SilentlyContinue

# 2. QR Modal Active
$temp2 = Join-Path $env:TEMP ("edge_cap2_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp2",
    "--window-size=1440,1150",
    "--screenshot=$out2",
    "http://localhost:3000/preview-founders-showcase.html?modal=qr&founder=salim"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp2 -Recurse -Force -ErrorAction SilentlyContinue

# 3. Lightbox with 4K toolbar
$temp3 = Join-Path $env:TEMP ("edge_cap3_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp3",
    "--window-size=1440,1200",
    "--screenshot=$out3",
    "http://localhost:3000/preview-founders-showcase.html?modal=lightbox&founder=assets/founder-banner-salim.jpg"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp3 -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Card with 4K/QR: $(Test-Path $out1)"
Write-Host "QR Modal: $(Test-Path $out2)"
Write-Host "Lightbox Toolbar: $(Test-Path $out3)"
