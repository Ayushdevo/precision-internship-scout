import csv
from io import StringIO
import pytest
from jobs import fetch_vetted_jobs
from exports import export_matches_csv
@pytest.mark.parametrize('url', ['javascript:alert(1)', 'https://user:pass@example.test', 'https://example.test:invalid'])
def test_export_does_not_include_links_rejected_by_the_ui(url):
    jobs = fetch_vetted_jobs('')
    jobs[0]['target_link'] = url
    rows = list(csv.DictReader(StringIO(export_matches_csv(jobs, 'Python'))))
    assert rows[0]['careers_url'] == ''
    assert rows[1]['careers_url'] == jobs[1]['target_link']
