# Recruitment Tool

A lightweight recruitment management tool to track job openings, candidates, and hiring pipelines.

## Features

- Post and manage job openings
- Track candidate applications and status
- Move candidates through pipeline stages (Applied → Screening → Interview → Offer → Hired/Rejected)
- Add notes and scores per candidate
- Export candidate data to CSV

## Project Structure

```
recruitment-tool/
├── src/
│   ├── models/          # Data models (Job, Candidate, Application)
│   ├── services/        # Business logic
│   └── utils/           # Helpers (CSV export, validators)
├── tests/               # Unit tests
├── data/                # Sample seed data
└── main.py              # CLI entry point
```

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
git clone https://github.com/ankitthakkar/recruitment-tool.git
cd recruitment-tool
pip install -r requirements.txt
```

### Usage

```bash
# Add a job opening
python main.py jobs add --title "Software Engineer" --department "Engineering" --location "Remote"

# List all open jobs
python main.py jobs list

# Add a candidate
python main.py candidates add --name "Jane Doe" --email "jane@example.com" --job-id 1

# Advance a candidate to the next stage
python main.py candidates advance --id 3

# Export candidates to CSV
python main.py export --output candidates.csv
```

## Pipeline Stages

| Stage      | Description                        |
|------------|------------------------------------|
| Applied    | Application received               |
| Screening  | Initial resume/phone screen        |
| Interview  | Technical or panel interview       |
| Offer      | Offer extended                     |
| Hired      | Candidate accepted and onboarded   |
| Rejected   | Not moving forward                 |

## Contributing

Pull requests are welcome. Please open an issue first to discuss major changes.

## License

MIT
