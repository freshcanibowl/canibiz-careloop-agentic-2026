# Deploy Now — Windows / PowerShell

Run from the repository root.

## 1. Login
```powershell
gcloud auth login
gcloud auth application-default login
```

## 2. Deploy Cloud Run + Firestore
```powershell
.\scripts\deploy_gcp.ps1 -ProjectId "YOUR_GCP_PROJECT_ID"
```

## 3. Gemini authentication
Cloud Run uses its `careloop-runtime` service account with Vertex AI ADC.
No Gemini API key is required.

## 4. Run live proof
```powershell
.\scripts\run_live_proof.ps1 `
  -CareLoopUrl "https://YOUR-SERVICE-URL.run.app"
```

Expected final line:
```text
LIVE PROOF PASS
```

## 5. Capture evidence
Screenshot:
- Cloud Run service page
- Firestore `careloop_tasks`
- terminal `LIVE PROOF PASS`
- `/health` JSON showing firestore + gemini + Gemini 3.5+

## Important
The current demo persists task state and structured observation history in Firestore. Cloud Run permits up to three instances. Use synthetic demo data only: authentication and tenant isolation are still required before a real pilot.
