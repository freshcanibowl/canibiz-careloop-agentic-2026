param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [Parameter(Mandatory=$true)][Security.SecureString]$GeminiApiKey,
  [string]$Region = "asia-southeast1",
  [string]$Service = "canibiz-careloop-agent"
)

$ErrorActionPreference = "Stop"

function Invoke-GCloud {
  & gcloud @args
  if ($LASTEXITCODE -ne 0) {
    throw "gcloud failed with exit code $LASTEXITCODE"
  }
}

Invoke-GCloud config set project $ProjectId

$Secret = "careloop-gemini-api-key"

$exists = $true
try { Invoke-GCloud secrets describe $Secret | Out-Null } catch { $exists = $false }

if (-not $exists) {
  Invoke-GCloud secrets create $Secret --replication-policy="automatic"
}

$Bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($GeminiApiKey)
try {
  $PlainGeminiApiKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($Bstr)
  $PlainGeminiApiKey | & gcloud secrets versions add $Secret --data-file=-
  if ($LASTEXITCODE -ne 0) { throw "Unable to add Gemini secret version" }
} finally {
  $PlainGeminiApiKey = $null
  [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($Bstr)
}

$SaEmail = "careloop-runtime@$ProjectId.iam.gserviceaccount.com"
Invoke-GCloud secrets add-iam-policy-binding $Secret `
  --member="serviceAccount:$SaEmail" `
  --role="roles/secretmanager.secretAccessor" | Out-Null

Invoke-GCloud run services update $Service `
  --region $Region `
  --set-secrets "GEMINI_API_KEY=$Secret`:latest"

$Url = & gcloud run services describe $Service --region $Region --format="value(status.url)"
if ($LASTEXITCODE -ne 0) { throw "Unable to resolve deployed service URL" }
Write-Host "Secret wired. Service URL: $Url"
