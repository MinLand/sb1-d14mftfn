from dataclasses import dataclass
from typing import List

@dataclass
class DoctorKnowledge:
    a_drug: int
    d_drug: int
    generic: int
    learn_low: List[str]
    learn_high: List[str]
    event_no: List[str]
    event_low: List[str]
    event_high: List[str]
    decision_weight: float