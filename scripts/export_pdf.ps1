$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$outPdf = "i:\I-Ai\App\S&R CoreSync Solutions\Project\assets\SR-CoreSync-Corporate-Profile-2026.pdf"
$url = "http://localhost:3000/corporate-profile.html"

Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--print-to-pdf=$outPdf",
    "--no-pdf-header-footer",
    $url
) -Wait

Start-Sleep -Seconds 1
Write-Host "PDF Exists: $(Test-Path $outPdf)"
Write-Host "PDF Size: $((Get-Item $outPdf).Length / 1KB) KB"
