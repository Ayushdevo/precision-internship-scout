"""Escaped presentation helpers for potentially external job data."""
from html import escape
from urllib.parse import urlsplit


def safe_careers_url(value: str) -> str | None:
    if not isinstance(value, str) or any(char.isspace() for char in value):
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            return None
        return value
    except ValueError:
        return None


def render_job_card(job: dict, score: int, matched: list[str]) -> str:
    badges = "".join(
        f'<span class="req-badge">{"✓" if req in matched else "✗"} {escape(str(req))}</span>'
        for req in job["requirements"]
    )
    style = "success" if score >= 90 else "info" if score >= 75 else "warning"
    return (
        '<div class="job-card"><div class="job-card-header"><div>'
        f'<h3 class="job-card-title">{escape(str(job["company"]))} — {escape(str(job["title"]))}</h3>'
        f'<div class="job-card-meta">{escape(str(job["location"]))}</div></div>'
        f'<span class="match-tag match-tag-{style}">{int(score)}% keyword coverage</span></div>'
        f'<div>{badges}</div></div>'
    )
