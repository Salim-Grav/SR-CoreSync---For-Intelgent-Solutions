$temp = Join-Path $env:TEMP ("edge_walkthrough_" + [Guid]::NewGuid().ToString())
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$out = "C:\Users\msali\.gemini\antigravity-ide\brain\1778519a-9b5a-4358-b8ed-35a118f691af\live_project_walkthrough.png"
$url = "http://localhost:3000/index.html"

Start-Process $edge -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp",
    "--window-size=1440,960",
    "--screenshot=$out",
    $url
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue

if (Test-Path $out) {
    Write-Host "SNAPSHOT_SUCCESS: $out"
} else {
    Write-Host "SNAPSHOT_FAILED"
}
