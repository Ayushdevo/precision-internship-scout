import pytest
from scoring import compute_dynamic_match
@pytest.mark.parametrize('requirement,profile', [('C', 'C++'), ('C', 'C#'), ('C++', 'C+++')])
def test_other_language_tokens_do_not_count_as_evidence(requirement, profile):
    assert compute_dynamic_match([requirement], profile)[0] == 0
@pytest.mark.parametrize('requirement,profile', [('C', 'C, Python'), ('C++', 'C++/Python'), ('C#', '(C#)'), ('Python', 'Python.')])
def test_punctuation_delimited_language_evidence_still_matches(requirement, profile):
    assert compute_dynamic_match([requirement], profile)[0] == 100
