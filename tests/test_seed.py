from src.services.recruitment_service import RecruitmentService
from data.seed import seed


def test_seed_creates_expected_jobs():
    svc = seed(RecruitmentService())
    jobs = svc.list_jobs(open_only=False)
    assert len(jobs) == 3


def test_seed_creates_expected_candidates():
    svc = seed(RecruitmentService())
    candidates = svc.list_candidates()
    assert len(candidates) == 5


def test_seed_candidate_stages():
    svc = seed(RecruitmentService())
    alice = svc.get_candidate(1)
    assert alice.stage == "Interview"
    assert alice.score == 9

    carol = svc.get_candidate(3)
    assert carol.stage == "Rejected"

    david = svc.get_candidate(4)
    assert david.stage == "Offer"
