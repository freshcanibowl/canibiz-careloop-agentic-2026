# 4-Minute Demo Script

## 0:00–0:30 — Problem
Veterinary follow-up is fragmented across conversations and memory. CareLoop turns a vet's plan into trackable owner actions and a concise professional follow-up brief.

## 0:30–1:05 — Vet creates plan
Show Pika's seven-day transition plan. CareLoop decomposes it into structured follow-up tasks and persists them.

## 1:05–1:45 — Owner reports naturally
Enter: "Pika's poop was softer today, around 5. She finished her food and has not vomited."
Show Gemini converting this into stool=5, appetite=normal, vomiting=false. Explain that model output is validated before state mutation.

## 1:45–2:25 — Agent acts
Advance workflow time. Show overdue observations becoming `FOLLOW_UP_REQUIRED` and CareLoop emitting `REQUEST_OWNER_FOLLOW_UP`.
This is the agentic action: it changes workflow state and creates a next action rather than merely answering a question.

## 2:25–3:05 — Safety boundary
Show deterministic routing. CareLoop does not diagnose or prescribe; concerning observations route to professional review.

## 3:05–3:35 — VetBrief
Show adherence, longitudinal owner observations, missing actions, and review status in one concise brief.

## 3:35–4:00 — Architecture + value
Show Google ADK + Gemini 3.5+ + Firestore + Cloud Run architecture.
Close with the three pilot KPIs: consultation follow-up time saved, home-to-clinic information completeness, and owner follow-up completion.
