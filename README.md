# CaniBiz CareLoop Agent

CareLoop is an autonomous veterinary follow-up workflow for the **Taskmaster** category of the All Things Agentic Hackathon. It turns a vet care plan into persistent owner tasks, structures natural-language home observations with Gemini 3.5 Flash, detects missing actions, applies deterministic safety routing, and produces a concise VetBrief for professional review.

CareLoop is a workflow aid. It does not diagnose, prescribe, or replace veterinary judgment.

## What works

- Vet care plan to typed follow-up tasks
- Firestore-backed task persistence
- Firestore-backed structured observation history
- Gemini 3.5 Flash observation structuring through Vertex AI
- Google GenAI SDK and Google ADK integration boundaries
- Contract validation before model output changes workflow state
- Missing-action detection with `REQUEST_OWNER_FOLLOW_UP`
- Deterministic routing to `CONTINUE_MONITORING` or `PROFESSIONAL_REVIEW_REQUIRED`
- Longitudinal VetBrief rendering
- Responsive owner-facing workflow UI at `/`
- Downloadable plain-text VetBrief for professional handoff
- FastAPI service deployed to Google Cloud Run

## Architecture

The API runs on Cloud Run. The runtime service account calls Gemini 3.5 Flash through Vertex AI Application Default Credentials and reads or writes task state in Firestore. Gemini structures owner language; deterministic Python services remain authoritative for workflow state and safety routing.

See:

- `docs/architecture.png` — uploadable architecture diagram
- `docs/architecture.mmd` — diagram source
- `docs/demo_script_4min.md` — demo outline

## Local setup

Prerequisites:

- Python 3.11 or newer
- A PowerShell or POSIX-compatible terminal

Create and activate a virtual environment if desired, then install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the regression suite and file preflight:

```powershell
python -m pytest -q
python scripts\preflight.py
```

Expected verified result:

```text
20 passed
PRE-SUBMISSION FILE PREFLIGHT PASS
```

The Google client library may emit a Python deprecation warning; it does not affect the test result.

## Local API

The default local runtime uses in-memory task storage and the deterministic observation parser:

```powershell
uvicorn app.api:app --host 127.0.0.1 --port 8080
```

Open:

```text
http://127.0.0.1:8080/
http://127.0.0.1:8080/health
http://127.0.0.1:8080/docs
```

The root UI runs the complete care-plan → owner update → agent follow-up → VetBrief workflow against the same API used by the live proof.

For a reproducible walkthrough, click `Run guided demo`. It executes the real four-stage cloud workflow once, stops on any error, and enables the VetBrief download only after completion.

## Google Cloud deployment

Authenticate:

```powershell
gcloud auth login
gcloud auth application-default login
```

Deploy Cloud Run, Firestore, Vertex AI configuration, and the least-privilege runtime service account:

```powershell
.\scripts\deploy_gcp.ps1 -ProjectId "YOUR_GCP_PROJECT_ID"
```

The deployed service uses:

- `CARELOOP_STORAGE_BACKEND=firestore`
- `CARELOOP_AI_BACKEND=gemini`
- `GEMINI_MODEL=gemini-3.5-flash`
- Vertex AI Application Default Credentials

No Gemini API key is required in the final Cloud Run runtime.

## Reproducible live proof

Run against the deployed service:

```powershell
.\scripts\run_live_proof.ps1 `
  -CareLoopUrl "https://YOUR-SERVICE-URL.run.app"
```

The proof creates a unique plan and verifies:

1. the health endpoint reports Firestore, Gemini, Gemini 3.5 Flash, and the active Cloud Run revision;
2. care-plan tasks are created and persisted;
3. Gemini structures a natural-language owner observation;
4. overdue requirements create follow-up actions;
5. VetBrief renders accumulated workflow evidence.

Only accept the run when the final line is:

```text
LIVE PROOF PASS
```

## API workflow

- `GET /health`
- `POST /plans`
- `POST /observations`
- `POST /follow-up/check`
- `POST /vetbrief`

Interactive request schemas are available from the FastAPI `/docs` endpoint.

## Safety and privacy

- Do not send real personal, veterinary, or confidential data to the public demo.
- Gemini output is validated and is never authoritative for diagnosis or treatment.
- Safety decisions are deterministic workflow-routing examples, not clinically validated diagnostic rules.
- Production deployments should add authentication before accepting real users.

## Production boundary

Task state and structured observation history are persisted in Firestore. The deploy script permits up to three Cloud Run instances. The public hackathon service intentionally has no end-user authentication, so it must use synthetic demo data only; authentication, tenant isolation, audit retention, and clinical validation remain required before a real pilot.

## Evidence

- `scripts/live_proof.py` — fail-fast end-to-end proof
- `scripts/render_live_proof_evidence.ps1` — renders the verified proof summary
- `docs/evidence/live-proof-pass.png` — current Cloud Run live-proof evidence
- `docs/evidence/live-ui-workflow.png` — public owner-facing workflow completion state
- `docs/design/careloop-workspace-concept.png` — accepted UI concept
- `docs/design/careloop-workspace-render.png` — browser-verified desktop implementation
- `docs/design/careloop-workspace-mobile.png` — browser-verified mobile implementation
- `docs/devpost_proof_checklist.md` — evidence capture list
- `docs/current_ship_gate.md` — proof gate and limitations
- `docs/gemini_contract.md` — structured model boundary
- `docs/pilot_scorecard.md` — proposed pilot measurements
