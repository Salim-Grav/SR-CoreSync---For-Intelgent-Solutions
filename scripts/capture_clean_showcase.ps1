$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\6c3789a5-12b8-47a7-ae30-f1a347854cd7"
$outImg = Join-Path $artDir "live_clean_showcase_preview.png"
$temp = Join-Path $env:TEMP ("edge_cap_clean_" + [Guid]::NewGuid().ToString())

$args = @(
    "--headless=new",
    "--user-data-dir=$temp",
    "--window-size=1280,1050",
    "--screenshot=$outImg",
    "http://localhost:3000/preview-founders-showcase.html"
)

Start-Process -FilePath $edgePath -ArgumentList $args -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Success: $(Test-Path $outImg)"
