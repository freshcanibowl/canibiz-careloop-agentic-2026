# Build #3 — Agentic Contract

CareLoop may autonomously:
- detect an overdue required observation;
- change that task from `PENDING` to `FOLLOW_UP_REQUIRED`;
- emit an auditable `REQUEST_OWNER_FOLLOW_UP` action.

CareLoop may not autonomously:
- diagnose disease;
- prescribe treatment;
- change deterministic safety policy;
- claim causality from an owner-reported observation.

The safety gate only routes workflow state to professional review.
