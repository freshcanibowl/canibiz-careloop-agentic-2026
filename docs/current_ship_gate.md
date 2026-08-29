# Current Ship Gate

Local:
- 19 tests passing
- pre-submission file preflight passing

Verified live:
1. Cloud Run service deployed
2. Firestore task persistence proven
3. Firestore structured observation persistence deployed
4. Gemini 3.5 Flash live structuring proven through Vertex AI
5. revision `canibiz-careloop-agent-00005-h9g` passed full `scripts/live_proof.py` with `LIVE PROOF PASS`
6. revision `canibiz-careloop-agent-00006-2z2` serves the responsive owner-facing UI at `/`
7. public UI completed plan → Gemini observation → follow-up → VetBrief against Firestore
8. desktop 1536×1024 and mobile 390×844 layouts checked in Browser
9. revision `canibiz-careloop-agent-00006-2z2` passed the scripted `LIVE PROOF PASS` gate

Verified live on revision `canibiz-careloop-agent-00007-fvm`:
- VetBrief download is disabled until a real brief is generated
- generated backend-rendered brief downloads as a plan-scoped `.txt` handoff
- public runtime reports Firestore persistence

Verified live on revision `canibiz-careloop-agent-00008-md6`:
- one click executed all four real cloud stages without manual intervention
- 11 tasks, Gemini structured observation, two follow-up actions, VetBrief, and download gate verified
- refreshed `docs/evidence/live-ui-workflow.png` captures the completed guided demo

Still required before final submission:
1. public demo video URL
2. final screenshots, including Cloud Run and Firestore console evidence
3. architecture PNG upload during the later submission phase

Production boundary:
- task state and structured observation history persist in Firestore.
- the deploy script permits up to three Cloud Run instances.
- the public demo uses synthetic data only; production still requires authentication, tenant isolation, audit retention, and clinical validation.
