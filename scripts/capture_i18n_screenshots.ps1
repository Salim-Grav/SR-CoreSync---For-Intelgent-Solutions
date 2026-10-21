$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) { $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\fb165293-a382-4790-9d97-89e32247a0a7"

function Capture-Page($url, $filename, $scroll = 0) {
    $out = Join-Path $artDir $filename
    $temp = Join-Path $env:TEMP ("edge_" + [Guid]::NewGuid().ToString())
    Start-Process $edgePath -ArgumentList @(
        "--headless=new",
        "--user-data-dir=$temp",
        "--window-size=1440,900",
        "--screenshot=$out",
        "--ignore-certificate-errors",
        "--virtual-time-budget=5000",
        $url
    ) -Wait
    Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "OK: $out"
}

Capture-Page "http://127.0.0.1:8765/nl/index.html#work"    "nl_work_platforms.png"
Capture-Page "http://127.0.0.1:8765/en/index.html#work"    "en_work_platforms.png"
Capture-Page "http://127.0.0.1:8765/de/index.html#work"    "de_work_platforms.png"
