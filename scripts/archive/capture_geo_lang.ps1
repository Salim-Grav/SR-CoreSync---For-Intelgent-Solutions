$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$artDir = "C:\Users\msali\.gemini\antigravity-ide\brain\fb165293-a382-4790-9d97-89e32247a0a7"

function Capture-GeoLang($url, $browserLang, $outName, $width=1440, $height=950) {
    $outPath = Join-Path $artDir $outName
    $tempDir = Join-Path $env:TEMP ("edge_geolang_" + [Guid]::NewGuid().ToString())
    
    Start-Process $edgePath -ArgumentList @(
        "--headless=new",
        "--lang=$browserLang",
        "--user-data-dir=$tempDir",
        "--window-size=$width,$height",
        "--screenshot=$outPath",
        "--virtual-time-budget=3500",
        $url
    ) -Wait
    
    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Captured: $outPath with lang: $browserLang"
}

# 1. Dutch visitor lands on Arabic index.html -> Suggest switch to Nederlands
Capture-GeoLang "file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/index.html" "nl-NL" "geolang_banner_nl_on_ar.png" 1440 950

# 2. Arabic visitor lands on English index.html -> Suggest switch to Arabic
Capture-GeoLang "file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/en/index.html" "ar-SA" "geolang_banner_ar_on_en.png" 1440 950

# 3. German visitor lands on Dutch index.html -> Suggest switch to Deutsch
Capture-GeoLang "file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/nl/index.html" "de-DE" "geolang_banner_de_on_nl.png" 1440 950
