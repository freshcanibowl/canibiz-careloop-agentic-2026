param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [string]$Region = "asia-southeast1",
  [string]$Service = "canibiz-careloop-agent",
  [string]$FirestoreLocation = "asia-southeast1"
)

$ErrorActionPreference = "Stop"

function Invoke-GCloud {
  & gcloud @args
  if ($LASTEXITCODE -ne 0) {
    throw "gcloud failed with exit code $LASTEXITCODE"
  }
}

Write-Host "==> Using project $ProjectId"
Invoke-GCloud config set project $ProjectId

Write-Host "==> Enabling required APIs"
Invoke-GCloud services enable `
  run.googleapis.com `
  cloudbuild.googleapis.com `
  artifactregistry.googleapis.com `
  firestore.googleapis.com `
  aiplatform.googleapis.com

Write-Host "==> Ensuring Firestore database exists"
try {
  Invoke-GCloud firestore databases describe --database="(default)" | Out-Null
} catch {
  Invoke-GCloud firestore databases create --database="(default)" --location=$FirestoreLocation --type=firestore-native
}

Write-Host "==> Creating service account if needed"
$SaName = "careloop-runtime"
$SaEmail = "$SaName@$ProjectId.iam.gserviceaccount.com"
try {
  Invoke-GCloud iam service-accounts describe $SaEmail | Out-Null
} catch {
  Invoke-GCloud iam service-accounts create $SaName --display-name="CaniBiz CareLoop Runtime"
}

Write-Host "==> Granting minimum Firestore access"
Invoke-GCloud projects add-iam-policy-binding $ProjectId `
  --member="serviceAccount:$SaEmail" `
  --role="roles/datastore.user" | Out-Null

Write-Host "==> Granting Vertex AI inference access"
Invoke-GCloud projects add-iam-policy-binding $ProjectId `
  --member="serviceAccount:$SaEmail" `
  --role="roles/aiplatform.user" | Out-Null

Write-Host "==> Deploying Cloud Run from source"
Invoke-GCloud run deploy $Service `
  --source . `
  --region $Region `
  --platform managed `
  --allow-unauthenticated `
  --service-account $SaEmail `
  --max-instances 1 `
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$ProjectId,GOOGLE_CLOUD_LOCATION=global,GOOGLE_GENAI_USE_VERTEXAI=true,CARELOOP_STORAGE_BACKEND=firestore,CARELOOP_AI_BACKEND=gemini,GEMINI_MODEL=gemini-3.5-flash"

Write-Host "==> Removing legacy Gemini API key mount"
Invoke-GCloud run services update $Service `
  --region $Region `
  --remove-secrets GEMINI_API_KEY

$Url = & gcloud run services describe $Service --region $Region --format="value(status.url)"
if ($LASTEXITCODE -ne 0) { throw "Unable to resolve deployed service URL" }
Write-Host ""
Write-Host "DEPLOYED: $Url"
Write-Host "Next: run scripts/live_proof.py"
