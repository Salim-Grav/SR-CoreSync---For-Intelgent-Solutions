$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}
$outImg = "C:\Users\msali\.gemini\antigravity-ide\brain\d456d906-1802-455f-affc-b1880d9cb803\live_banner_showcase.png"
$url = "http://localhost:3000/preview-founders-showcase.html"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--disable-gpu",
    "--user-data-dir=$tempDir",
    "--window-size=1440,900",
    "--screenshot=$outImg",
    $url
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
if (Test-Path $outImg) {
    Write-Host "SUCCESS: Captured $outImg with size $((Get-Item $outImg).Length) bytes"
} else {
    Write-Host "FAILED: Could not capture $outImg"
}
