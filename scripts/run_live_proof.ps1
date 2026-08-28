param(
  [Parameter(Mandatory=$true)][string]$CareLoopUrl
)
$ErrorActionPreference = "Stop"
$env:CARELOOP_URL = $CareLoopUrl.TrimEnd("/")
python scripts/live_proof.py
