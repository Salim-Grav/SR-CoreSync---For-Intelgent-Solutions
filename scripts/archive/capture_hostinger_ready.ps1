$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$outImg = "C:\Users\msali\.gemini\antigravity-ide\brain\98021c3f-b2d7-4399-9020-5c36ee97997e\live_hostinger_ready_production.png"
$url = "http://127.0.0.1:3000/index.html"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1440,1080",
    "--screenshot=$outImg",
    $url
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

if (Test-Path $outImg) {
    Write-Host "SNAPSHOT_SUCCESS: $outImg"
} else {
    Write-Host "SNAPSHOT_FAILED"
}
