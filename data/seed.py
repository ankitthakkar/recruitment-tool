"""Seed the recruitment service with sample data for development and demos."""
from src.services.recruitment_service import RecruitmentService


def seed(svc: RecruitmentService) -> RecruitmentService:
    # Jobs
    svc.add_job("Software Engineer", "Engineering", "Remote",
                "Build backend services and APIs.")
    svc.add_job("Product Manager", "Product", "San Francisco",
                "Own the roadmap and work cross-functionally.")
    svc.add_job("Data Analyst", "Data", "New York",
                "Turn data into actionable insights.")

    # Candidates for job 1
    c1 = svc.add_candidate("Alice Nguyen", "alice@example.com", 1)
    svc.advance_candidate(c1.id)   # Screening
    svc.advance_candidate(c1.id)   # Interview
    svc.score_candidate(c1.id, 9, "Excellent system design skills")

    c2 = svc.add_candidate("Bob Kim", "bob@example.com", 1)
    svc.advance_candidate(c2.id)   # Screening
    svc.score_candidate(c2.id, 6, "Decent experience, needs growth")

    c3 = svc.add_candidate("Carol Smith", "carol@example.com", 1)
    svc.reject_candidate(c3.id)

    # Candidates for job 2
    c4 = svc.add_candidate("David Lee", "david@example.com", 2)
    svc.advance_candidate(c4.id)   # Screening
    svc.advance_candidate(c4.id)   # Interview
    svc.advance_candidate(c4.id)   # Offer
    svc.score_candidate(c4.id, 10, "Outstanding fit")

    c5 = svc.add_candidate("Eva Patel", "eva@example.com", 2)

    return svc


if __name__ == "__main__":
    from tabulate import tabulate

    service = seed(RecruitmentService())

    print("\n=== Jobs ===")
    rows = [[j.id, j.title, j.department, j.location] for j in service.list_jobs(open_only=False)]
    print(tabulate(rows, headers=["ID", "Title", "Department", "Location"]))

    print("\n=== Candidates ===")
    rows = [[c.id, c.name, c.job_id, c.stage, c.score or "—"] for c in service.list_candidates()]
    print(tabulate(rows, headers=["ID", "Name", "Job", "Stage", "Score"]))
