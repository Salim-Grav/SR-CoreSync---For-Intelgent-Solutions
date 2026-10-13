$staging = "C:\Users\msali\AppData\Local\Temp\taxsync_staging"
if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging -Force | Out-Null

$zip = "I:\I-Ai\App\S&R CoreSync Solutions\Project\downloads\SR-TaxSync-Desktop-v2.4-Setup.zip"
$exe = "I:\I-Ai\App\S&R CoreSync Solutions\Project\downloads\SR-TaxSync-Setup-v2.4.exe"

Expand-Archive -Path $zip -DestinationPath $staging -Force
Copy-Item $exe -Destination $staging -Force
Remove-Item $zip -Force

Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $zip -Force
Remove-Item $staging -Recurse -Force
Write-Host "ZIP rebuilt successfully with EXE included!"
