from dataclasses import dataclass

@dataclass(frozen=True)
class AgentAction:
    action_type: str
    pet_id: str
    day: int
    reason: str
    target_task_id: str | None = None
