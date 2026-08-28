# Devpost Proof Checklist

## Must capture from LIVE deployment
- Cloud Run service URL and healthy deployment.
- `/health` response showing:
  - `storage_backend = firestore`
  - `ai_backend = gemini`
  - Gemini 3.5+ model.
- Vet plan creating persistent tasks.
- Owner free-text transformed into typed observation by Gemini.
- Missing required action producing `REQUEST_OWNER_FOLLOW_UP`.
- VetBrief generated from accumulated workflow state.
- Firestore console showing persisted CareLoop task documents.
- Google Cloud console showing Cloud Run service.

## Claims we can make only after live proof
- Deployed on Google Cloud Run.
- Persistent workflow state stored in Firestore.
- Gemini 3.5+ used for live owner-language structuring.

## Claims we should NOT make
- Veterinary diagnosis.
- Autonomous treatment/prescribing.
- Clinical validation.
- Proven time savings before real veterinary timing study.
