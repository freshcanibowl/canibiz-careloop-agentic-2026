import json
import os
import sys
import urllib.request
from uuid import uuid4

BASE = os.environ.get("CARELOOP_URL", "").rstrip("/")
if not BASE:
    raise SystemExit("Set CARELOOP_URL to the deployed Cloud Run URL")
PLAN_ID = f"proof-pika-{uuid4().hex[:12]}"

def request(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())

def show(label, value):
    print(f"\n=== {label} ===")
    print(json.dumps(value, indent=2, default=str))

health = request("GET", "/health")
show("1 HEALTH", health)
assert health["status"] == "ok"
assert health["storage_backend"] == "firestore"
assert health["ai_backend"] == "gemini"
assert health["gemini_model"].startswith("gemini-3.5")

plan = {
    "plan_id": PLAN_ID,
    "pet_id": "pet-pika",
    "instructions": "Transition food over 7 days. Record stool daily. Monitor appetite and vomiting. Review after 7 days.",
    "start_date": "2026-08-28",
    "review_date": "2026-09-04"
}
created = request("POST", "/plans", plan)
show("2 PLAN -> PERSISTED TASKS", created)
assert len(created["tasks"]) >= 10

observation = request("POST", "/observations", {
    "plan_id": PLAN_ID,
    "pet_id": "pet-pika",
    "day": 3,
    "message": "Pika's poop was softer today, around 5. She finished her food and has not vomited."
})
show("3 GEMINI -> STRUCTURED OBSERVATION", observation)
assert observation["observation"]["stool_score"] == 5
assert observation["observation"]["appetite"] == "normal"
assert observation["observation"]["vomiting"] is False

actions = request("POST", "/follow-up/check", {
    "plan_id": PLAN_ID,
    "current_day": 4
})
show("4 AGENTIC FOLLOW-UP ACTIONS", actions)
assert len(actions["actions"]) >= 1

brief = request("POST", "/vetbrief", {
    "plan_id": PLAN_ID,
    "pet_id": "pet-pika",
    "through_day": 3
})
show("5 VETBRIEF", brief)
assert "FOLLOW-UP ADHERENCE" in brief["rendered"]

print("\nLIVE PROOF PASS")
