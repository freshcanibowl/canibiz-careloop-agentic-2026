from dataclasses import dataclass, field

@dataclass(frozen=True)
class VetBrief:
    pet_id: str
    plan_id: str
    adherence_percent: int
    completed_tasks: int
    expected_owner_tasks: int
    outstanding_tasks: tuple[str, ...] = field(default_factory=tuple)
    safety_status: str = "CONTINUE_MONITORING"
    safety_reasons: tuple[str, ...] = field(default_factory=tuple)
    longitudinal_summary: tuple[str, ...] = field(default_factory=tuple)
