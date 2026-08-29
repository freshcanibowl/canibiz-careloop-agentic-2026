# Current Ship Gate

Local:
- 20 tests passing
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

Verified live on revision `canibiz-careloop-agent-00009-vvz`:
- `/health` exposes the active Cloud Run revision alongside Firestore and Gemini runtime metadata
- the public workflow evidence panel displays `revision 00009-vvz`
- the UI and health endpoint now provide a direct deployment-to-proof audit trail
- a fresh guided demo completed on 29 Aug 2026 and produced final product/result reference frames
- authenticated read-only Cloud Run and Firestore control-plane configuration is captured in `docs/evidence/cloud-control-plane.md`

Still required before final submission:
1. record and publish the public demo video
2. optionally capture Google Cloud Console screenshots to supplement the reproducible CLI control-plane evidence
3. upload the selected screenshots and architecture PNG during the later submission phase

Production boundary:
- task state and structured observation history persist in Firestore.
- the deploy script permits up to three Cloud Run instances.
- the public demo uses synthetic data only; production still requires authentication, tenant isolation, audit retention, and clinical validation.
