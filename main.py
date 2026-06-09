import click
from tabulate import tabulate

from src.services import store

svc = store.load()


@click.group()
def cli():
    """Recruitment Tool — manage jobs and candidates from the command line."""


# ── Jobs ──────────────────────────────────────────────────────────────────────

@cli.group()
def jobs():
    """Manage job openings."""


@jobs.command("add")
@click.option("--title", required=True)
@click.option("--department", required=True)
@click.option("--location", required=True)
@click.option("--description", default="")
def jobs_add(title, department, location, description):
    job = svc.add_job(title, department, location, description)
    store.save(svc)
    click.echo(f"Created job #{job.id}: {job.title} ({job.department}) — {job.location}")


@jobs.command("list")
@click.option("--all", "show_all", is_flag=True, help="Include closed jobs")
def jobs_list(show_all):
    job_list = svc.list_jobs(open_only=not show_all)
    if not job_list:
        click.echo("No jobs found.")
        return
    rows = [[j.id, j.title, j.department, j.location, "Open" if j.open else "Closed"] for j in job_list]
    click.echo(tabulate(rows, headers=["ID", "Title", "Department", "Location", "Status"]))


@jobs.command("close")
@click.argument("job_id", type=int)
def jobs_close(job_id):
    if svc.close_job(job_id):
        store.save(svc)
        click.echo(f"Job #{job_id} closed.")
    else:
        click.echo(f"Job #{job_id} not found.", err=True)


# ── Candidates ────────────────────────────────────────────────────────────────

@cli.group()
def candidates():
    """Manage candidates."""


@candidates.command("add")
@click.option("--name", required=True)
@click.option("--email", required=True)
@click.option("--job-id", required=True, type=int)
def candidates_add(name, email, job_id):
    candidate = svc.add_candidate(name, email, job_id)
    if not candidate:
        click.echo(f"Job #{job_id} not found.", err=True)
        return
    store.save(svc)
    click.echo(f"Added candidate #{candidate.id}: {candidate.name} for job #{job_id}")


@candidates.command("list")
@click.option("--job-id", type=int, default=None)
@click.option("--stage", default=None)
def candidates_list(job_id, stage):
    candidate_list = svc.list_candidates(job_id=job_id, stage=stage)
    if not candidate_list:
        click.echo("No candidates found.")
        return
    rows = [[c.id, c.name, c.email, c.job_id, c.stage, c.score or "—"] for c in candidate_list]
    click.echo(tabulate(rows, headers=["ID", "Name", "Email", "Job", "Stage", "Score"]))


@candidates.command("advance")
@click.argument("candidate_id", type=int)
def candidates_advance(candidate_id):
    new_stage = svc.advance_candidate(candidate_id)
    if new_stage is None:
        click.echo(f"Candidate #{candidate_id} not found.", err=True)
    else:
        store.save(svc)
        click.echo(f"Candidate #{candidate_id} moved to: {new_stage}")


@candidates.command("reject")
@click.argument("candidate_id", type=int)
def candidates_reject(candidate_id):
    if svc.reject_candidate(candidate_id):
        store.save(svc)
        click.echo(f"Candidate #{candidate_id} marked as Rejected.")
    else:
        click.echo(f"Candidate #{candidate_id} not found.", err=True)


@candidates.command("score")
@click.argument("candidate_id", type=int)
@click.option("--score", required=True, type=int)
@click.option("--notes", default="")
def candidates_score(candidate_id, score, notes):
    try:
        if svc.score_candidate(candidate_id, score, notes):
            store.save(svc)
            click.echo(f"Candidate #{candidate_id} scored {score}/10.")
        else:
            click.echo(f"Candidate #{candidate_id} not found.", err=True)
    except ValueError as e:
        click.echo(str(e), err=True)


# ── Export ────────────────────────────────────────────────────────────────────

@cli.command("export")
@click.option("--output", required=True, help="Output CSV file path")
@click.option("--job-id", type=int, default=None)
def export(output, job_id):
    csv_data = svc.export_candidates_csv(job_id=job_id)
    with open(output, "w", newline="") as f:
        f.write(csv_data)
    click.echo(f"Exported to {output}")


if __name__ == "__main__":
    cli()
