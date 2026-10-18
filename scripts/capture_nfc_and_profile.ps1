$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\6c3789a5-12b8-47a7-ae30-f1a347854cd7"
$outNfcSalim = Join-Path $artDir "live_nfc_card_salim.png"
$outNfcRaed = Join-Path $artDir "live_nfc_card_raed.png"
$outProfileP1 = Join-Path $artDir "live_corporate_profile_doc.png"

# 1. Capture Salim NFC Mobile View (480x1000)
$temp1 = Join-Path $env:TEMP ("edge_cap_nfc1_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp1",
    "--window-size=480,1050",
    "--screenshot=$outNfcSalim",
    "http://localhost:3000/card.html?id=salim"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp1 -Recurse -Force -ErrorAction SilentlyContinue

# 2. Capture Raed NFC Mobile View (480x1000)
$temp2 = Join-Path $env:TEMP ("edge_cap_nfc2_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp2",
    "--window-size=480,1050",
    "--screenshot=$outNfcRaed",
    "http://localhost:3000/card.html?id=raed"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp2 -Recurse -Force -ErrorAction SilentlyContinue

# 3. Capture Corporate Profile Document View (1200x1400)
$temp3 = Join-Path $env:TEMP ("edge_cap_nfc3_" + [Guid]::NewGuid().ToString())
Start-Process $edgePath -ArgumentList @(
    "--headless=new",
    "--user-data-dir=$temp3",
    "--window-size=1200,1400",
    "--screenshot=$outProfileP1",
    "http://localhost:3000/corporate-profile.html"
) -Wait
Start-Sleep -Milliseconds 600
Remove-Item -Path $temp3 -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Salim NFC: $(Test-Path $outNfcSalim)"
Write-Host "Raed NFC: $(Test-Path $outNfcRaed)"
Write-Host "Corporate Profile: $(Test-Path $outProfileP1)"
