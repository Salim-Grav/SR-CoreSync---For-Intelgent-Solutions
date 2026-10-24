$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\6c3789a5-12b8-47a7-ae30-f1a347854cd7"
$outSlider = Join-Path $artDir "live_4k_qr_showcase_slider.png"
$outQr = Join-Path $artDir "live_4k_qr_modal_salim.png"
$outLight = Join-Path $artDir "live_4k_qr_lightbox.png"

# 1. Slider with 4K & QR buttons
$temp0 = Join-Path $env:TEMP ("edge_cap0_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp0",
    "--window-size=1440,1150",
    "--screenshot=$outSlider",
    "http://localhost:3000/preview-founders-showcase.html?view=slider"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp0 -Recurse -Force -ErrorAction SilentlyContinue

# 2. QR Modal Triggered
# Create a small temp HTML or script that triggers openQrModal('salim')
$temp1 = Join-Path $env:TEMP ("edge_cap1_" + [Guid]::NewGuid().ToString())
# We can use a test page or add query param ?testQr=salim
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp1",
    "--window-size=1440,1150",
    "--screenshot=$outQr",
    "http://localhost:3000/preview-founders-showcase.html?modal=qr&founder=salim"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp1 -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Slider: $(Test-Path $outSlider)"
Write-Host "QR Modal: $(Test-Path $outQr)"
