import re
from app.models.observation import StructuredObservation

def parse_owner_observation(pet_id: str, day: int, message: str) -> StructuredObservation:
    text = message.lower()
    stool_score = None
    if "stool" in text or "poop" in text:
        m = re.search(r"\b([1-7])\b", text)
        stool_score = int(m.group(1)) if m else None

    appetite = None
    if any(x in text for x in ("appetite normal","normal appetite","finished her food","finished his food","ate normally")):
        appetite = "normal"
    elif any(x in text for x in ("poor appetite","ate less","didn't finish","did not finish")):
        appetite = "low"

    vomiting = None
    if any(x in text for x in ("hasn't vomited","has not vomited","no vomiting","didn't vomit","did not vomit")):
        vomiting = False
    elif any(x in text for x in ("vomited","vomiting","threw up")):
        vomiting = True

    return StructuredObservation(pet_id, day, stool_score, appetite, vomiting)
