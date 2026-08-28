from pathlib import Path
required = [
    "app/agent.py",
    "app/api.py",
    "app/adapters/gemini_observation.py",
    "app/adapters/firestore_repository.py",
    "Dockerfile",
    "docs/architecture.mmd",
    "docs/demo_script_4min.md",
    "docs/devpost_proof_checklist.md",
    "scripts/live_proof.py",
]
missing = [x for x in required if not Path(x).exists()]
if missing:
    raise SystemExit("Missing: " + ", ".join(missing))
print("PRE-SUBMISSION FILE PREFLIGHT PASS")
