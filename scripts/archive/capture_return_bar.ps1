$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) { $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\fb165293-a382-4790-9d97-89e32247a0a7"

function Capture-Page($url, $file, $h=950) {
    $out = Join-Path $artDir $file
    $temp = Join-Path $env:TEMP ("cap_" + [Guid]::NewGuid().ToString())
    Start-Process $edgePath -ArgumentList @(
        "--headless=new",
        "--user-data-dir=$temp",
        "--window-size=1440,$h",
        "--screenshot=$out",
        "--virtual-time-budget=3000",
        $url
    ) -Wait
    Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Captured: $out"
}

Capture-Page "http://127.0.0.1:8765/preview-work.html" "preview_work_with_return_bar.png" 950
Capture-Page "http://127.0.0.1:8765/preview-software.html" "preview_software_with_return_bar.png" 950
