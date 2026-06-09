import pytest
from src.services.recruitment_service import RecruitmentService


@pytest.fixture
def svc():
    return RecruitmentService()


@pytest.fixture
def svc_with_job(svc):
    svc.add_job("Software Engineer", "Engineering", "Remote")
    return svc


class TestJobs:
    def test_add_job(self, svc):
        job = svc.add_job("Designer", "Product", "NYC")
        assert job.id == 1
        assert job.title == "Designer"
        assert job.open is True

    def test_list_jobs_open_only(self, svc):
        svc.add_job("Job A", "Eng", "Remote")
        svc.add_job("Job B", "HR", "NYC")
        svc.close_job(1)
        assert len(svc.list_jobs(open_only=True)) == 1
        assert len(svc.list_jobs(open_only=False)) == 2

    def test_close_job(self, svc):
        job = svc.add_job("Analyst", "Finance", "London")
        assert svc.close_job(job.id) is True
        assert job.open is False

    def test_close_nonexistent_job(self, svc):
        assert svc.close_job(999) is False


class TestCandidates:
    def test_add_candidate(self, svc_with_job):
        c = svc_with_job.add_candidate("Alice", "alice@example.com", 1)
        assert c is not None
        assert c.name == "Alice"
        assert c.stage == "Applied"

    def test_add_candidate_invalid_job(self, svc):
        c = svc.add_candidate("Bob", "bob@example.com", 99)
        assert c is None

    def test_advance_candidate(self, svc_with_job):
        c = svc_with_job.add_candidate("Carol", "carol@example.com", 1)
        new_stage = svc_with_job.advance_candidate(c.id)
        assert new_stage == "Screening"

    def test_advance_through_full_pipeline(self, svc_with_job):
        c = svc_with_job.add_candidate("Dan", "dan@example.com", 1)
        stages = []
        for _ in range(4):
            stage = svc_with_job.advance_candidate(c.id)
            stages.append(stage)
        assert stages == ["Screening", "Interview", "Offer", "Hired"]

    def test_advance_past_terminal_stage(self, svc_with_job):
        c = svc_with_job.add_candidate("Eve", "eve@example.com", 1)
        c.stage = "Hired"
        result = c.advance()
        assert result is False
        assert c.stage == "Hired"

    def test_reject_candidate(self, svc_with_job):
        c = svc_with_job.add_candidate("Frank", "frank@example.com", 1)
        assert svc_with_job.reject_candidate(c.id) is True
        assert c.stage == "Rejected"

    def test_score_candidate(self, svc_with_job):
        c = svc_with_job.add_candidate("Grace", "grace@example.com", 1)
        svc_with_job.score_candidate(c.id, 8, "Strong problem solver")
        assert c.score == 8
        assert c.notes == "Strong problem solver"

    def test_score_out_of_range(self, svc_with_job):
        c = svc_with_job.add_candidate("Heidi", "heidi@example.com", 1)
        with pytest.raises(ValueError):
            svc_with_job.score_candidate(c.id, 11)

    def test_filter_by_stage(self, svc_with_job):
        svc_with_job.add_candidate("Ivan", "ivan@example.com", 1)
        c2 = svc_with_job.add_candidate("Judy", "judy@example.com", 1)
        svc_with_job.advance_candidate(c2.id)
        applied = svc_with_job.list_candidates(stage="Applied")
        screening = svc_with_job.list_candidates(stage="Screening")
        assert len(applied) == 1
        assert len(screening) == 1


class TestExport:
    def test_export_csv(self, svc_with_job):
        svc_with_job.add_candidate("Karl", "karl@example.com", 1)
        csv_output = svc_with_job.export_candidates_csv()
        assert "Karl" in csv_output
        assert "Applied" in csv_output
        assert "email" in csv_output  # header row
