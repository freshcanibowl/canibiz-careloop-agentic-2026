# Final Demo Narration — English

Target duration: 3 minutes 40 seconds to 3 minutes 55 seconds. Use the hosted product first, then the architecture and proof frames.

## 0:00–0:28 — Problem

Veterinary follow-up is often fragmented across discharge notes, messages, and memory. Owners may miss daily actions or describe changes inconsistently, while care teams spend time reconstructing what happened at home. CareLoop turns that gap into an accountable follow-up workflow.

## 0:28–1:05 — Plan to persistent tasks

This is the live CareLoop service on Google Cloud Run. The page confirms Cloud Connected, Firestore persistence, Gemini 3.5 Flash, and the deployed revision. I will run the guided demo once. CareLoop converts Pika's seven-day veterinary plan into eleven typed tasks covering stool observations, appetite, vomiting, and the food transition. These tasks are persisted in Firestore rather than held only in the browser.

## 1:05–1:42 — Natural language to validated structure

The owner reports naturally: Pika's poop was softer today, around five. She finished her food and has not vomited. Gemini 3.5 Flash, called through Vertex AI with the Google GenAI SDK, structures that message into stool score five, normal appetite, and no vomiting. Model output is treated as untrusted input and must pass a typed contract before it can change workflow state. The validated observation is also persisted.

## 1:42–2:18 — Agentic follow-up

CareLoop now compares required actions with accumulated evidence. Two stool observations are overdue, so the agent emits two explicit REQUEST_OWNER_FOLLOW_UP actions. This is more than a conversational answer: the system inspects state, identifies missing work, and creates the next action in an auditable workflow.

## 2:18–2:48 — Safety boundary

Gemini structures owner language, but it does not control clinical routing. Deterministic services remain authoritative. This synthetic observation routes to CONTINUE_MONITORING. Concerning evidence would route to professional review. CareLoop never diagnoses, prescribes, or replaces veterinary judgment.

## 2:48–3:22 — VetBrief

The final step generates a VetBrief with adherence, a longitudinal summary, outstanding tasks, and safety status. The brief can be downloaded as a backend-rendered handoff for professional review. The demo has now completed all four live stages without manual intervention.

## 3:22–3:52 — Architecture and close

CareLoop runs on Cloud Run, persists tasks and observations in Firestore, and calls Gemini 3.5 Flash through Vertex AI. Google ADK defines the orchestration boundary, while deterministic Python services protect workflow and safety decisions. The pilot value is measurable: less follow-up coordination time, more complete home-to-clinic information, and higher owner task completion. CareLoop makes follow-up accountable while keeping clinical authority with veterinary professionals.
