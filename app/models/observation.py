from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class StructuredObservation:
    pet_id: str
    day: int
    stool_score: Optional[int] = None
    appetite: Optional[str] = None
    vomiting: Optional[bool] = None
    source: str = "owner_report"
