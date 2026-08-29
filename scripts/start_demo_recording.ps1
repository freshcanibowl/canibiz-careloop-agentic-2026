param(
    [string]$CareLoopUrl = "https://canibiz-careloop-agent-kep7hzbbeq-as.a.run.app",
    [string]$ExpectedRevision = "canibiz-careloop-agent-00009-vvz",
    [switch]$ValidateOnly
)

$ErrorActionPreference = "Stop"
$baseUrl = $CareLoopUrl.TrimEnd("/")

Write-Host "==> Checking the public demo runtime"
$health = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get

if ($health.status -ne "ok") {
    throw "Health check did not return status=ok."
}
if ($health.storage_backend -ne "firestore") {
    throw "Expected Firestore, received $($health.storage_backend)."
}
if ($health.ai_backend -ne "gemini" -or $health.gemini_model -ne "gemini-3.5-flash") {
    throw "Expected Gemini 3.5 Flash runtime."
}
if ($health.revision -ne $ExpectedRevision) {
    throw "Expected revision $ExpectedRevision, received $($health.revision)."
}

$edgeCandidates = @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
)
$edgePath = $edgeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $edgePath) {
    throw "Microsoft Edge was not found. Open $baseUrl manually in a clean browser window."
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$narrationPath = Join-Path $repoRoot "docs\demo_narration_en.md"

Write-Host ""
Write-Host "RUNTIME READY: $($health.revision)"
Write-Host "1. Press Win+Alt+R to start Windows Game Bar recording."
Write-Host "2. Click Run guided demo once and follow docs/demo_narration_en.md."
Write-Host "3. Press Win+Alt+R again after the architecture/proof closing frame."
Write-Host "4. Find the MP4 in your Windows Videos\Captures folder."
Write-Host ""

if ($ValidateOnly) {
    Write-Host "VALIDATION PASS"
    return
}

Start-Process -FilePath "notepad.exe" -ArgumentList $narrationPath
Start-Process -FilePath $edgePath -ArgumentList @(
    "--app=$baseUrl",
    "--window-size=1440,900",
    "--force-device-scale-factor=1"
)
