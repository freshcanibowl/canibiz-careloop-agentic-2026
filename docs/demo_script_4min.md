# 4-Minute Demo Script

## 0:00–0:30 — Problem
Veterinary follow-up is fragmented across conversations and memory. CareLoop turns a vet's plan into trackable owner actions and a concise professional follow-up brief.

## 0:30–1:05 — Vet creates plan
Open the hosted root page and click **Run guided demo**. As Step 1 runs, show Pika's seven-day transition plan. CareLoop decomposes it into 11 structured follow-up tasks and persists them in Firestore.

## 1:05–1:45 — Owner reports naturally
As Step 2 runs, show the seeded owner sentence: "Pika's poop was softer today, around 5. She finished her food and has not vomited."
Show Gemini converting this into stool=5, appetite=normal, vomiting=false. Explain that model output is validated before state mutation and the observation is persisted.

## 1:45–2:25 — Agent acts
As Step 3 runs, show overdue observations and CareLoop emitting `REQUEST_OWNER_FOLLOW_UP`.
This is the agentic action: it changes workflow state and creates a next action rather than merely answering a question.

## 2:25–3:05 — Safety boundary
Show deterministic routing. CareLoop does not diagnose or prescribe; concerning observations route to professional review.

## 3:05–3:35 — VetBrief
As Step 4 finishes, show adherence, longitudinal owner observations, missing actions, and review status in one concise brief. Click **Download VetBrief** to demonstrate the professional handoff artifact.

## 3:35–4:00 — Architecture + value
Show Google ADK + Gemini 3.5+ + Firestore + Cloud Run architecture.
Close with the three pilot KPIs: consultation follow-up time saved, home-to-clinic information completeness, and owner follow-up completion.

## Recording guardrails

- Use only the synthetic Pika fixture shown in the UI.
- Start from a fresh page so the guided demo creates a unique plan ID.
- Keep the notice area visible while each numbered step runs.
- Do not cut away until the final notice says `Guided demo complete`.
- Show `Cloud Connected` and `Firestore persisted` before starting.
- If any step reports `Guided demo stopped`, stop recording and rerun from a fresh page; do not edit around a failed live call.
