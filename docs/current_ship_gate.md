# Current Ship Gate

Local:
- 13 tests passing
- pre-submission file preflight passing

Verified live:
1. Cloud Run service deployed
2. Firestore task persistence proven
3. Gemini 3.5 Flash live structuring proven through Vertex AI
4. full `scripts/live_proof.py` pass with `LIVE PROOF PASS`

Still required for the Devpost packet:
1. public or properly shared repository URL
2. public demo video URL
3. evidence screenshots captured
4. submitter type and project start date confirmed
5. architecture PNG uploaded

Known limitation:
- observation history for VetBrief remains process-memory.
- Cloud Run deploy script pins max instances to 1 for deterministic hackathon proof.
- this must be disclosed; production hardening should persist observations too.
