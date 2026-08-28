# Google Cloud deployment — production wiring

Required production environment:
- `CARELOOP_STORAGE_BACKEND=firestore`
- `CARELOOP_AI_BACKEND=gemini`
- `GEMINI_MODEL=gemini-3.5-flash`
- `GOOGLE_CLOUD_PROJECT=<project-id>`

Deploy:
```bash
gcloud run deploy canibiz-careloop-agent   --source .   --region asia-southeast1   --allow-unauthenticated   --set-env-vars CARELOOP_STORAGE_BACKEND=firestore,CARELOOP_AI_BACKEND=gemini,GEMINI_MODEL=gemini-3.5-flash
```

Smoke test:
```bash
curl "$CARELOOP_URL/health"
```

The health response must report:
- `storage_backend: firestore`
- `ai_backend: gemini`
- `gemini_model: gemini-3.5-flash`

Then create a plan, submit an owner observation, run `/follow-up/check`, and request `/vetbrief`.

Important: current demo observations are process-memory in the API; hackathon proof must
demonstrate task state persistence in Firestore. Persisting observations themselves is the
next hardening step if time permits.
