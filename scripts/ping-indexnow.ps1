# ============================================================
# IndexNow ping for the Agnostic Framework (PowerShell version)
# ------------------------------------------------------------
# Notifies Bing + Yandex + Seznam + Naver instantly that the
# framework has new or updated content. Single ping covers all
# IndexNow-participating search engines.
#
# Usage:
#   .\scripts\ping-indexnow.ps1                      # ping the default high-traffic surfaces
#   .\scripts\ping-indexnow.ps1 <url1> <url2> ...    # ping specific URLs
#
# Examples:
#   .\scripts\ping-indexnow.ps1
#     # → pings: homepage, timeline, llms.txt, llms-full.txt,
#     #         manifest.json, both animated artifacts
#
#   .\scripts\ping-indexnow.ps1 `
#     "https://a70m123r.github.io/agnostic-framework/continuations/28.md" `
#     "https://a70m123r.github.io/agnostic-framework/CHANGELOG.md"
#     # → pings just those two URLs
#
# If PowerShell blocks execution: run once
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#
# IndexNow API spec: https://www.indexnow.org
# ============================================================

param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ExtraUrls)

$Key = "568fa5e82cc4459dabbfa57d220d26d8"
$Host = "a70m123r.github.io"
$KeyLocation = "https://$Host/agnostic-framework/$Key.txt"
$Endpoint = "https://api.indexnow.org/IndexNow"

# Default URL set — high-traffic surfaces that change often
$DefaultUrls = @(
  "https://a70m123r.github.io/agnostic-framework/",
  "https://a70m123r.github.io/agnostic-framework/timeline/",
  "https://a70m123r.github.io/agnostic-framework/llms.txt",
  "https://a70m123r.github.io/agnostic-framework/llms-full.txt",
  "https://a70m123r.github.io/agnostic-framework/manifest.json",
  "https://a70m123r.github.io/agnostic-framework/primitives.json",
  "https://a70m123r.github.io/agnostic-framework/CHANGELOG.md",
  "https://a70m123r.github.io/agnostic-framework/for-agents/",
  "https://a70m123r.github.io/agnostic-framework/artifacts/wrapper_overlap_animated.html",
  "https://a70m123r.github.io/agnostic-framework/artifacts/michotte_launching_extension.html"
)

# Use args if provided, otherwise defaults
if ($ExtraUrls -and $ExtraUrls.Count -gt 0) {
  $Urls = $ExtraUrls
} else {
  $Urls = $DefaultUrls
}

$Body = @{
  host        = $Host
  key         = $Key
  keyLocation = $KeyLocation
  urlList     = $Urls
} | ConvertTo-Json

Write-Host "Pinging IndexNow with $($Urls.Count) URL(s)..." -ForegroundColor Cyan
Write-Host "Key location: $KeyLocation" -ForegroundColor Gray
Write-Host ""

try {
  $Response = Invoke-WebRequest -Uri $Endpoint `
    -Method POST `
    -ContentType "application/json; charset=utf-8" `
    -Body $Body `
    -UseBasicParsing `
    -ErrorAction Stop

  switch ($Response.StatusCode) {
    200 { Write-Host "[OK] Success (HTTP 200): URLs accepted for indexing" -ForegroundColor Green }
    202 { Write-Host "[OK] Accepted (HTTP 202): URLs received; key validation pending" -ForegroundColor Green }
    default { Write-Host "[?] Unexpected status (HTTP $($Response.StatusCode))" -ForegroundColor Yellow }
  }
} catch [System.Net.WebException] {
  $StatusCode = [int]$_.Exception.Response.StatusCode
  $Reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
  $ErrorBody = $Reader.ReadToEnd()

  switch ($StatusCode) {
    400 { Write-Host "[FAIL] Bad request (HTTP 400): malformed JSON or invalid URL format" -ForegroundColor Red }
    403 { Write-Host "[FAIL] Forbidden (HTTP 403): key validation failed — confirm $KeyLocation returns the key string" -ForegroundColor Red }
    422 { Write-Host "[FAIL] Unprocessable (HTTP 422): URLs don't match the verified host, or other validation issue" -ForegroundColor Red }
    429 { Write-Host "[FAIL] Too many requests (HTTP 429): rate-limited; back off and retry" -ForegroundColor Red }
    default { Write-Host "[FAIL] HTTP $StatusCode" -ForegroundColor Red }
  }
  Write-Host $ErrorBody -ForegroundColor DarkRed
  exit 1
}

Write-Host ""
Write-Host "URLs pinged:" -ForegroundColor Gray
foreach ($u in $Urls) { Write-Host "  $u" -ForegroundColor Gray }
Write-Host ""
Write-Host "Note: IndexNow ping notifies Bing + Yandex + Seznam + Naver simultaneously." -ForegroundColor DarkGray
Write-Host "      Each engine independently decides when to crawl. Typical surface time: minutes to hours." -ForegroundColor DarkGray
