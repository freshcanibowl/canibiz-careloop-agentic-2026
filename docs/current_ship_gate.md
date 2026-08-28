# Current Ship Gate

Local:
- 17 tests passing
- pre-submission file preflight passing

Verified live:
1. Cloud Run service deployed
2. Firestore task persistence proven
3. Firestore structured observation persistence deployed
4. Gemini 3.5 Flash live structuring proven through Vertex AI
5. revision `canibiz-careloop-agent-00005-h9g` passed full `scripts/live_proof.py` with `LIVE PROOF PASS`

Still required before final submission:
1. public demo video URL
2. final screenshots, including Cloud Run and Firestore console evidence
3. architecture PNG upload during the later submission phase

Production boundary:
- task state and structured observation history persist in Firestore.
- the deploy script permits up to three Cloud Run instances.
- the public demo uses synthetic data only; production still requires authentication, tenant isolation, audit retention, and clinical validation.
