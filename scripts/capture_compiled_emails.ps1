$tempDir = Join-Path $env:TEMP ("edge_cap_" + [Guid]::NewGuid().ToString())
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$invoiceFile = "file:///" + (Resolve-Path "dist\emails\invoice-quote-compiled.html").Path.Replace("\", "/")
$welcomeFile = "file:///" + (Resolve-Path "dist\emails\welcome-email-compiled.html").Path.Replace("\", "/")

$outInvoice = "C:\Users\msali\.gemini\antigravity-ide\brain\c343b500-bda0-4fad-aa48-4c2182879e6c\live_compiled_invoice_email.png"
$outWelcome = "C:\Users\msali\.gemini\antigravity-ide\brain\c343b500-bda0-4fad-aa48-4c2182879e6c\live_compiled_welcome_email.png"

# Capture Invoice
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1200,1050",
    "--screenshot=$outInvoice",
    $invoiceFile
) -Wait

Start-Sleep -Seconds 1

# Capture Welcome
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$tempDir",
    "--window-size=1200,1050",
    "--screenshot=$outWelcome",
    $welcomeFile
) -Wait

Start-Sleep -Seconds 1
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Both compiled email snapshots captured successfully."
