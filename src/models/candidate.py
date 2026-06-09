from dataclasses import dataclass, field
from datetime import date
from typing import Optional

PIPELINE_STAGES = ["Applied", "Screening", "Interview", "Offer", "Hired", "Rejected"]


@dataclass
class Candidate:
    id: int
    name: str
    email: str
    job_id: int
    stage: str = "Applied"
    score: Optional[int] = None  # 1–10
    notes: str = ""
    applied_at: date = field(default_factory=date.today)

    def advance(self) -> bool:
        """Move to the next stage. Returns False if already at a terminal stage."""
        terminal = {"Hired", "Rejected"}
        if self.stage in terminal:
            return False
        idx = PIPELINE_STAGES.index(self.stage)
        self.stage = PIPELINE_STAGES[idx + 1]
        return True

    def reject(self):
        self.stage = "Rejected"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "job_id": self.job_id,
            "stage": self.stage,
            "score": self.score,
            "notes": self.notes,
            "applied_at": str(self.applied_at),
        }
