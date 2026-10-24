$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}
$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$outImg1 = "C:\Users\msali\.gemini\antigravity-ide\brain\0fa97aaa-2c0d-46de-bd13-ab949ab18753\index_founders_slider_panoramic.png"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,2400",
    "--screenshot=$outImg1",
    "http://localhost:3000/index.html"
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

if (Test-Path $outImg1) {
    Write-Host "SUCCESS: $outImg1"
} else {
    Write-Host "FAILED"
}
