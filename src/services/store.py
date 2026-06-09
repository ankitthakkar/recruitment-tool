"""Simple JSON file-based persistence for the recruitment service."""
import json
import os
from datetime import date
from typing import Any

from src.models.candidate import Candidate
from src.models.job import Job
from src.services.recruitment_service import RecruitmentService

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "db.json")


def _parse_date(val):
    return date.fromisoformat(val) if val else None


def load(path: str = DEFAULT_PATH) -> RecruitmentService:
    svc = RecruitmentService()
    if not os.path.exists(path):
        return svc
    with open(path) as f:
        data = json.load(f)
    for j in data.get("jobs", []):
        job = Job(
            id=j["id"],
            title=j["title"],
            department=j["department"],
            location=j["location"],
            description=j.get("description", ""),
            open=j["open"],
            created_at=_parse_date(j["created_at"]),
            closing_date=_parse_date(j.get("closing_date")),
        )
        svc._jobs.append(job)
        svc._job_id_seq = max(svc._job_id_seq, job.id + 1)
    for c in data.get("candidates", []):
        candidate = Candidate(
            id=c["id"],
            name=c["name"],
            email=c["email"],
            job_id=c["job_id"],
            stage=c["stage"],
            score=c.get("score"),
            notes=c.get("notes", ""),
            applied_at=_parse_date(c["applied_at"]),
        )
        svc._candidates.append(candidate)
        svc._candidate_id_seq = max(svc._candidate_id_seq, candidate.id + 1)
    return svc


def save(svc: RecruitmentService, path: str = DEFAULT_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data: dict[str, Any] = {
        "jobs": [j.to_dict() for j in svc._jobs],
        "candidates": [c.to_dict() for c in svc._candidates],
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
