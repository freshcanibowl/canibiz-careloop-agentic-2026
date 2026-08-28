# Title

CaniBiz CareLoop Agent

## One-line Summary

An autonomous veterinary follow-up agent that turns a vet's care plan into persistent owner tasks, structures natural-language home observations with Gemini 3.5 Flash, detects missing actions, and produces a concise VetBrief for professional review.

## Problem

Veterinary follow-up is fragmented across discharge notes, chat messages, human memory, and incomplete home observations. Owners may forget daily actions or report changes in inconsistent language, while veterinary teams must reconstruct adherence and risk signals before deciding what needs attention.

## Solution

CareLoop converts a veterinary care plan into a typed, trackable follow-up workflow. It persists task state, accepts natural-language owner updates, validates Gemini's structured output before changing workflow state, detects overdue required actions, emits an explicit follow-up action, applies deterministic safety routing, and composes a longitudinal VetBrief for a veterinary professional.

The project is a Taskmaster entry: it completes a multi-step workflow and creates auditable next actions instead of stopping at a conversational answer.

## Why This Matters

Better follow-up information can reduce avoidable coordination work and give veterinary professionals a clearer picture of what happened at home. CareLoop is deliberately a workflow aid, not a diagnostic or prescribing system. Its safety boundary keeps clinical authority with the veterinary professional.

## How We Used AI

- Gemini 3.5 Flash runs through Vertex AI and the Google GenAI SDK.
- Gemini transforms free-text owner messages into a typed observation contract, including stool score, appetite, and vomiting status.
- Model output is treated as untrusted input and validated before any workflow mutation.
- Deterministic domain logic remains authoritative for task state, missing-action detection, and safety routing.
- A Google ADK orchestrator defines the agent boundary and explicitly prohibits diagnosis, prescribing, or overriding deterministic safety decisions.

Example live input:

> Pika's poop was softer today, around 5. She finished her food and has not vomited.

The deployed system structured this as stool score 5, normal appetite, and no vomiting during the live proof.

## How We Used Codex

Codex was used as an engineering collaborator throughout the build:

- decomposed the workflow into typed domain contracts and testable boundaries;
- followed test-driven development for care-plan decomposition, observation parsing, persistence, missing-action detection, safety routing, VetBrief generation, and Vertex AI runtime wiring;
- diagnosed Windows PowerShell and Google Cloud SDK execution-policy issues;
- helped migrate Gemini access from a Developer API key to Vertex AI Application Default Credentials so usage could run through the Google Cloud project;
- hardened Cloud Run, Firestore, IAM, deployment scripts, and the fail-fast live-proof runner;
- reran regression and submission preflight checks before drafting this packet.

No clinical claims were generated or accepted solely because an AI coding assistant proposed them.

## Key Features

1. **Care plan decomposition** — converts a time-bounded veterinary plan into structured follow-up tasks.
2. **Persistent task state** — stores task documents in Firestore.
3. **Natural-language observation intake** — uses Gemini 3.5 Flash to structure owner updates.
4. **Contract validation** — validates model output before applying it.
5. **Autonomous follow-up detection** — detects missing required observations and emits `REQUEST_OWNER_FOLLOW_UP`.
6. **Deterministic safety gate** — routes concerning observations to professional review without diagnosing or prescribing.
7. **VetBrief** — summarizes adherence, longitudinal observations, missing actions, and review status.
8. **Cloud proof surface** — exposes health, plan, observation, follow-up, and VetBrief endpoints on Cloud Run.

## Architecture

CareLoop is a FastAPI service deployed to Google Cloud Run.

1. A veterinary plan enters the Google ADK CareLoop orchestrator.
2. The deterministic domain core decomposes it into typed tasks.
3. Task state is persisted in Firestore.
4. Owner free text is sent to Gemini 3.5 Flash through Vertex AI using the Google GenAI SDK.
5. Typed contract validation protects the domain boundary.
6. Deterministic services update task state, detect missing actions, and apply safety routing.
7. The VetBrief builder renders accumulated workflow evidence for professional review.

Uploadable diagram: `docs/architecture.png`

Editable sources: `docs/architecture.html` and `docs/architecture.mmd`.

## Testing Instructions

### Local regression

Prerequisites: Python and the dependencies in `requirements.txt`.

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python scripts\preflight.py
```

Current verified result:

- `13 passed, 1 warning`
- `PRE-SUBMISSION FILE PREFLIGHT PASS`

### Live Cloud Run proof

```powershell
.\scripts\run_live_proof.ps1 `
  -CareLoopUrl "https://canibiz-careloop-agent-kep7hzbbeq-as.a.run.app"
```

The runner verifies:

1. Cloud Run health reports Firestore, Gemini, and Gemini 3.5 Flash.
2. A unique care plan creates and persists tasks.
3. Gemini structures the owner observation into the expected typed fields.
4. Missing required actions produce agentic follow-up actions.
5. VetBrief renders accumulated workflow state.
6. The final output is `LIVE PROOF PASS`.

No credentials are required for the public hackathon proof endpoint. This endpoint is a demonstration service and must not receive real personal, veterinary, or confidential data.

## Public Demo Link

https://canibiz-careloop-agent-kep7hzbbeq-as.a.run.app

## Public Repository Link

Target GitHub account: https://github.com/freshcanibowl

**TODO:** Add the final repository URL after the CareLoop repository is created under this account. A GitHub profile URL does not satisfy the official repository field.

## Demo Video

**TODO:** Add the public YouTube or Vimeo URL. The video must be public, in English or include English subtitles, and no longer than four minutes.

Suggested outline:

- 0:00–0:30 — fragmented veterinary follow-up problem
- 0:30–1:05 — create Pika's plan and persist tasks
- 1:05–1:45 — submit natural language and show Gemini's validated structure
- 1:45–2:25 — show overdue state and `REQUEST_OWNER_FOLLOW_UP`
- 2:25–3:05 — show deterministic safety boundary
- 3:05–3:35 — render VetBrief
- 3:35–4:00 — show Cloud Run, Firestore, architecture, and value

## Screenshot Shot List

1. Cloud Run service page showing the active CareLoop revision and service URL.
2. `/health` JSON showing `firestore`, `gemini`, and `gemini-3.5-flash`.
3. Terminal showing persisted tasks, structured observation, follow-up actions, VetBrief, and `LIVE PROOF PASS`.
4. Firestore console showing `careloop_tasks` documents.
5. Exported architecture diagram.

## Submission Readiness Notes

Verified today:

- Cloud Run deployment is live in project `ai-malaysia`.
- Vertex AI ADC is used; no Gemini API key is mounted in the final runtime.
- Task state is persisted in Firestore.
- Gemini 3.5 Flash structured the live owner message successfully.
- The live proof reached `LIVE PROOF PASS`.
- Local regression has 13 passing tests.
- Pre-submission file preflight passes.

Still required:

- public or properly shared repository URL;
- public demo video URL;
- evidence screenshots;
- public repository and demo-video URLs.

## Known Limitations

- Observation history used by VetBrief remains in process memory; task state is persisted in Firestore.
- Cloud Run is therefore capped at one instance for deterministic hackathon proof.
- This is not production-grade distributed state. A pilot should persist observation history before multi-instance scaling.
- The safety rules are workflow-routing examples, not clinically validated diagnostic rules.
- CareLoop does not diagnose, prescribe, or replace veterinary judgment.
- The current proof surface is API-first rather than a polished owner-facing UI.

## TODO Official Form Fields

- **Submitter Type:** Individuals.
- **Submitter country of residence:** Malaysia.
- **Category:** Taskmaster.
- **Organization name:** Absolute Global Resources PLT.
- **Project start date (MM-DD-YY):** 08-20-26.
- **Repository URL:** TODO — create a repository under https://github.com/freshcanibowl and use its full URL.
- **Reproducible Testing instructions in README:** Yes.
- **Hosted project URL:** https://canibiz-careloop-agent-kep7hzbbeq-as.a.run.app
- **Testing instructions:** Use the Local regression and Live Cloud Run proof sections above.
- **Google SDK:** Google GenAI SDK (google-genai) and Agent Development Kit (ADK).
- **Google Cloud services:** Cloud Run and Firestore. Vertex AI is also used for Gemini inference.
- **Architecture diagram:** `docs/architecture.png` — ready to upload.
- **Google AI models:** Gemini 3.5 Flash.
- **Startup Prize organization and corporate email:** Not opted in yet. If opting in, confirm that Absolute Global Resources PLT is incorporated and provide its corporate email address.
- **Bonus content URL:** Optional TODO.
- **Bonus social post URL:** Optional TODO; include `#AllThingsAgenticHackathon`.
