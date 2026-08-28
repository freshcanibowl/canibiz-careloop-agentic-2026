import os
from dataclasses import asdict
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.models.care_plan import CarePlan
from app.runtime import build_task_repository, build_observation_structurer
from app.services.task_state import apply_observation
from app.services.safety_gate import evaluate_observation
from app.services.followup_engine import detect_missing_actions
from app.services.vetbrief_builder import build_vetbrief
from app.services.vetbrief_renderer import render_vetbrief
from app.use_cases import create_follow_up_plan

app = FastAPI(title="CaniBiz CareLoop Agent", version="0.2.0")

_task_repo = None
_structurer = None
_observations: dict[str, list] = {}


def task_repo():
    global _task_repo
    if _task_repo is None:
        _task_repo = build_task_repository()
    return _task_repo


def structurer():
    global _structurer
    if _structurer is None:
        _structurer = build_observation_structurer()
    return _structurer


class PlanRequest(BaseModel):
    plan_id: str
    pet_id: str
    instructions: str
    start_date: date
    review_date: date


class ObservationRequest(BaseModel):
    plan_id: str
    pet_id: str
    day: int = Field(ge=1)
    message: str = Field(min_length=1)


class FollowUpCheckRequest(BaseModel):
    plan_id: str
    current_day: int = Field(ge=1)


class VetBriefRequest(BaseModel):
    plan_id: str
    pet_id: str
    through_day: int = Field(ge=1)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "careloop",
        "storage_backend": os.getenv("CARELOOP_STORAGE_BACKEND", "memory"),
        "ai_backend": os.getenv("CARELOOP_AI_BACKEND", "deterministic"),
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
    }


@app.post("/plans")
def create_plan(req: PlanRequest):
    plan = CarePlan(**req.model_dump())
    tasks = create_follow_up_plan(plan, task_repo())
    _observations.setdefault(req.plan_id, [])
    return {"tasks": tasks}


@app.post("/observations")
def submit_observation(req: ObservationRequest):
    tasks = task_repo().list_for_plan(req.plan_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="care plan not found")

    obs = structurer().structure(req.pet_id, req.day, req.message)
    updated = apply_observation(tasks, obs)

    # Persist mutated task state. Both adapters support save_dicts().
    if hasattr(task_repo(), "save_dicts"):
        task_repo().save_dicts(updated)

    _observations.setdefault(req.plan_id, []).append(obs)
    decision = evaluate_observation(obs)

    return {
        "observation": asdict(obs),
        "safety": asdict(decision),
    }


@app.post("/follow-up/check")
def follow_up_check(req: FollowUpCheckRequest):
    tasks = task_repo().list_for_plan(req.plan_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="care plan not found")
    actions = detect_missing_actions(tasks, req.current_day)
    if hasattr(task_repo(), "save_dicts"):
        task_repo().save_dicts(tasks)
    return {"actions": [asdict(x) for x in actions]}


@app.post("/vetbrief")
def vetbrief(req: VetBriefRequest):
    tasks = task_repo().list_for_plan(req.plan_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="care plan not found")
    brief = build_vetbrief(
        req.plan_id,
        req.pet_id,
        tasks,
        _observations.get(req.plan_id, []),
        req.through_day,
    )
    return {
        "brief": asdict(brief),
        "rendered": render_vetbrief(brief),
    }
