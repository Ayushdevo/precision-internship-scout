"""A sample listing must never look like a confirmed vacancy."""
from rendering import render_job_card


def card(**fields):
    job = {
        "company": "Example", "title": "AI Intern",
        "location": "Remote", "requirements": ["Python"],
        **fields,
    }
    return render_job_card(job, 100, ["Python"])


def test_demo_card_explicitly_marks_unverified_status():
    html = card(source_type="demo", verified=False)
    assert "Illustrative demo listing" in html
    assert "not verified" in html


def test_other_unverified_source_is_marked():
    assert "Unverified listing" in card(source_type="external", verified=False)


def test_verified_flag_does_not_add_unverified_badge():
    assert "Unverified listing" not in card(source_type="external", verified=True)
