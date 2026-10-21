$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\fb165293-a382-4790-9d97-89e32247a0a7"

function Capture-Url($url, $outName, $width=1440, $height=1100) {
    $outPath = Join-Path $artDir $outName
    $tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
    
    Start-Process $edgePath -ArgumentList @(
        "--headless=new",
        "--user-data-dir=$tempDir",
        "--window-size=$width,$height",
        "--screenshot=$outPath",
        "--virtual-time-budget=2500",
        $url
    ) -Wait
    
    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Captured: $outPath"
}

Capture-Url "file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/preview-whitelabel-calculator.html?platform=healthbridge" "preview_whitelabel_calc_healthbridge.png" 1440 1200
Capture-Url "file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/preview-software.html" "preview_software_with_calc_btn.png" 1440 1100
