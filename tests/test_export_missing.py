"""Unknown job fields must not be rendered as the word 'None'."""
import csv
from io import StringIO

from exports import export_matches_csv


def test_missing_company_writes_empty_csv_field():
    jobs = [{
        "company": None,
        "title": "AI Intern",
        "location": "Remote",
        "requirements": [],
        "target_link": "https://example.org/careers",
    }]
    row = next(csv.DictReader(StringIO(export_matches_csv(jobs, "Python"))))
    assert row["company"] == ""
    assert row["title"] == "AI Intern"
