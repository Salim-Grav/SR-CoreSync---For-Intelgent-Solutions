$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\0fa97aaa-2c0d-46de-bd13-ab949ab18753"
$outAr = Join-Path $artDir "live_showcase_ar_badges.png"
$outEn = Join-Path $artDir "live_showcase_en_badges.png"
$outNl = Join-Path $artDir "live_showcase_nl_badges.png"

# Capture AR
$tempDirAr = Join-Path $env:TEMP ("edge_cap_ar_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDirAr",
    "--window-size=1440,2400",
    "--screenshot=$outAr",
    "http://localhost:3000/index.html#founders-showcase"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDirAr -Recurse -Force -ErrorAction SilentlyContinue

# Capture EN
$tempDirEn = Join-Path $env:TEMP ("edge_cap_en_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDirEn",
    "--window-size=1440,2400",
    "--screenshot=$outEn",
    "http://localhost:3000/en/index.html#founders-showcase"
) -Wait
Start-Sleep -Milliseconds 600
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
Start-Sleep -Milliseconds 600
Remove-Item -Path $tempDirNl -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "AR Exists: $(Test-Path $outAr)"
Write-Host "EN Exists: $(Test-Path $outEn)"
Write-Host "NL Exists: $(Test-Path $outNl)"
