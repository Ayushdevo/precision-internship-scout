"""Match badges should represent the same unique requirements as scoring."""
from rendering import render_job_card
from scoring import compute_dynamic_match, normalize_requirements


def test_requirement_labels_trim_duplicate_case_spacing():
    assert normalize_requirements(["Python", " python ", " SQL  ", "sql", None, ""]) == ["Python", "SQL"]


def test_card_renders_one_badge_per_distinct_requirement():
    requirements = ["Python", " python ", "SQL", " sql ", ""]
    score, matched, missing = compute_dynamic_match(requirements, "Python")
    html = render_job_card({
        "company": "Example", "title": "AI Intern",
        "location": "Remote", "requirements": requirements,
        "source_type": "demo", "verified": False,
    }, score, matched)
    assert score == 50
    assert matched == ["Python"]
    assert missing == ["SQL"]
    assert html.count('class="req-badge"') == 2
    assert "✓ Python" in html
    assert "✗ SQL" in html
