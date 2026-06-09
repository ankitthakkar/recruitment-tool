import csv
import io
from typing import List, Optional

from src.models.candidate import Candidate
from src.models.job import Job


class RecruitmentService:
    def __init__(self):
        self._jobs: List[Job] = []
        self._candidates: List[Candidate] = []
        self._job_id_seq = 1
        self._candidate_id_seq = 1

    # --- Jobs ---

    def add_job(self, title: str, department: str, location: str, description: str = "") -> Job:
        job = Job(
            id=self._job_id_seq,
            title=title,
            department=department,
            location=location,
            description=description,
        )
        self._jobs.append(job)
        self._job_id_seq += 1
        return job

    def list_jobs(self, open_only: bool = True) -> List[Job]:
        if open_only:
            return [j for j in self._jobs if j.open]
        return list(self._jobs)

    def get_job(self, job_id: int) -> Optional[Job]:
        return next((j for j in self._jobs if j.id == job_id), None)

    def close_job(self, job_id: int) -> bool:
        job = self.get_job(job_id)
        if not job:
            return False
        job.close()
        return True

    # --- Candidates ---

    def add_candidate(self, name: str, email: str, job_id: int) -> Optional[Candidate]:
        if not self.get_job(job_id):
            return None
        candidate = Candidate(
            id=self._candidate_id_seq,
            name=name,
            email=email,
            job_id=job_id,
        )
        self._candidates.append(candidate)
        self._candidate_id_seq += 1
        return candidate

    def list_candidates(self, job_id: Optional[int] = None, stage: Optional[str] = None) -> List[Candidate]:
        result = self._candidates
        if job_id is not None:
            result = [c for c in result if c.job_id == job_id]
        if stage is not None:
            result = [c for c in result if c.stage == stage]
        return result

    def get_candidate(self, candidate_id: int) -> Optional[Candidate]:
        return next((c for c in self._candidates if c.id == candidate_id), None)

    def advance_candidate(self, candidate_id: int) -> Optional[str]:
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return None
        candidate.advance()
        return candidate.stage

    def reject_candidate(self, candidate_id: int) -> bool:
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return False
        candidate.reject()
        return True

    def score_candidate(self, candidate_id: int, score: int, notes: str = "") -> bool:
        if not 1 <= score <= 10:
            raise ValueError("Score must be between 1 and 10")
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return False
        candidate.score = score
        if notes:
            candidate.notes = notes
        return True

    # --- Export ---

    def export_candidates_csv(self, job_id: Optional[int] = None) -> str:
        candidates = self.list_candidates(job_id=job_id)
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=["id", "name", "email", "job_id", "stage", "score", "notes", "applied_at"],
        )
        writer.writeheader()
        for c in candidates:
            writer.writerow(c.to_dict())
        return output.getvalue()
