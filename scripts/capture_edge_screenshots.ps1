$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\fb165293-a382-4790-9d97-89e32247a0a7"

function Capture-Url($url, $outName, $width=1440, $height=950) {
    $outPath = Join-Path $artDir $outName
    $tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
    
    Start-Process $edgePath -ArgumentList @(
        "--headless=new",
        "--user-data-dir=$tempDir",
        "--window-size=$width,$height",
        "--screenshot=$outPath",
        "--virtual-time-budget=3000",
        $url
    ) -Wait
    
    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Captured: $outPath"
}

Capture-Url "http://127.0.0.1:8765/preview-work.html#platforms" "preview_work_platforms_direct.png"
Capture-Url "http://127.0.0.1:8765/preview-software.html" "preview_software_full_page.png" 1440 1800
Capture-Url "http://127.0.0.1:8765/index.html#work" "index_work_section.png"
