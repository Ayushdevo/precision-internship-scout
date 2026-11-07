"""CSV exports must not allow Unicode-hidden spreadsheet formulas."""
import csv
from io import StringIO
import pytest
from exports import export_matches_csv


@pytest.mark.parametrize("prefix", ["\ufeff", "\u200b", "\u2060", " \ufeff "])
def test_unicode_prefix_does_not_bypass_formula_escape(prefix):
    job = {
        "company": prefix + "=1+1",
        "title": "AI intern", "location": "Remote",
        "requirements": [], "target_link": "https://example.com/jobs",
    }
    row = next(csv.DictReader(StringIO(export_matches_csv([job], ""))))
    assert row["company"] == "'" + prefix + "=1+1"


def test_safe_csv_field_keeps_original_text():
    job = {
        "company": "Research Lab", "title": "Engineer",
        "location": "Remote", "requirements": [],
        "target_link": "https://example.com/jobs",
    }
    row = next(csv.DictReader(StringIO(export_matches_csv([job], ""))))
    assert row["company"] == "Research Lab"
