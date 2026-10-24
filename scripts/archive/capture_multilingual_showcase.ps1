$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\0fa97aaa-2c0d-46de-bd13-ab949ab18753"
$outEn = Join-Path $artDir "live_showcase_en.png"
$outNl = Join-Path $artDir "live_showcase_nl.png"

# Capture EN
$tempDirEn = Join-Path $env:TEMP ("edge_cap_en_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDirEn",
    "--window-size=1440,2400",
    "--screenshot=$outEn",
    "http://localhost:3000/en/index.html#founders-showcase"
) -Wait
Start-Sleep -Milliseconds 800
Remove-Item -Path $tempDirEn -Recurse -Force -ErrorAction SilentlyContinue

# Capture NL
$tempDirNl = Join-Path $env:TEMP ("edge_cap_nl_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDirNl",
    "--window-size=1440,2400",
    "--screenshot=$outNl",
    "http://localhost:3000/nl/index.html#founders-showcase"
) -Wait
Start-Sleep -Milliseconds 800
Remove-Item -Path $tempDirNl -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "EN Exists: $(Test-Path $outEn)"
Write-Host "NL Exists: $(Test-Path $outNl)"
