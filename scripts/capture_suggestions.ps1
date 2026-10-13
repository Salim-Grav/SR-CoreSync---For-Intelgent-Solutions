$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$artifactDir = "C:\Users\msali\.gemini\antigravity-ide\brain\b4adc775-45bf-4bfa-8d40-6a12a92a104c"

$targets = @(
    @{
        Url = "http://127.0.0.1:3000/preview-license-manager.html"
        Out = Join-Path $artifactDir "live_salim_license_manager.png"
        Size = "1400,1050"
    },
    @{
        Url = "http://127.0.0.1:3000/preview-checkout.html"
        Out = Join-Path $artifactDir "live_software_checkout_ideal.png"
        Size = "1400,1050"
    },
    @{
        Url = "http://127.0.0.1:3000/preview-software-modal.html"
        Out = Join-Path $artifactDir "live_software_modal_download.png"
        Size = "1400,980"
    }
)

foreach ($t in $targets) {
    $tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
    Write-Host "Capturing $($t.Url) -> $($t.Out)"
    Start-Process $edgePath -ArgumentList @(
        "--headless=new",
        "--user-data-dir=$tempDir",
        "--window-size=$($t.Size)",
        "--screenshot=$($t.Out)",
        $t.Url
    ) -Wait
    Start-Sleep -Milliseconds 600
    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    if (Test-Path $t.Out) {
        $size = (Get-Item $t.Out).Length
        Write-Host "SUCCESS: $($t.Out) ($size bytes)"
    } else {
        Write-Host "FAILED: $($t.Out)"
    }
}
