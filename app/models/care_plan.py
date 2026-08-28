from dataclasses import dataclass
from datetime import date
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FOLLOW_UP_REQUIRED = "FOLLOW_UP_REQUIRED"

@dataclass(frozen=True)
class CarePlan:
    plan_id: str
    pet_id: str
    instructions: str
    start_date: date
    review_date: date

@dataclass
class FollowUpTask:
    task_id: str
    plan_id: str
    pet_id: str
    kind: str
    instruction: str
    due_day: int
    status: TaskStatus = TaskStatus.PENDING
