from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Job:
    id: int
    title: str
    department: str
    location: str
    description: str = ""
    open: bool = True
    created_at: date = field(default_factory=date.today)
    closing_date: Optional[date] = None

    def close(self):
        self.open = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "department": self.department,
            "location": self.location,
            "description": self.description,
            "open": self.open,
            "created_at": str(self.created_at),
            "closing_date": str(self.closing_date) if self.closing_date else None,
        }
