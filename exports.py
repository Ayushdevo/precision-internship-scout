"""Portable export of sample matches without candidate resume content."""
import csv
from io import StringIO
from scoring import compute_dynamic_match
from rendering import safe_careers_url


def _cell(value):
    value = str(value)
    # Spreadsheet applications may evaluate formula-like CSV cells.
    return "'" + value if value.lstrip().startswith(("=", "+", "-", "@")) else value


def export_matches_csv(jobs: list[dict], profile_text: str) -> str:
    buffer = StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(["company", "title", "location", "keyword_coverage_percent", "matched_requirements", "missing_requirements", "source_type", "verified", "careers_url"])
    for job in jobs:
        score, matched, missing = compute_dynamic_match(job["requirements"], profile_text)
        writer.writerow([_cell(value) for value in [job["company"], job["title"], job["location"], score,
            "; ".join(matched), "; ".join(missing), job.get("source_type", "unknown"),
            job.get("verified", False), safe_careers_url(job["target_link"]) or ""]])
    return buffer.getvalue()

