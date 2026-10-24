$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\fb165293-a382-4790-9d97-89e32247a0a7"
$outPath = Join-Path $artDir "index_work_section_clean.png"
$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())

# Run Edge with a longer virtual time budget and specific target
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,1100",
    "--screenshot=$outPath",
    "--virtual-time-budget=8000",
    "http://127.0.0.1:8765/index.html#work"
) -Wait

Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Captured: $outPath"
