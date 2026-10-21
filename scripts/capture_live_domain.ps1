$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) { $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\fb165293-a382-4790-9d97-89e32247a0a7"
$out = Join-Path $artDir "live_domain_verification.png"
$temp = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp",
    "--window-size=1440,900",
    "--screenshot=$out",
    "--ignore-certificate-errors",
    "--virtual-time-budget=5000",
    "https://sr-coresync.com/"
) -Wait

Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Captured: $out"
