"""Search should handle pasted phrases with variable spacing and case."""
from jobs import fetch_vetted_jobs


def test_multiword_queries_normalize_spacing_and_case():
    matches = fetch_vetted_jobs("  AI  \t ENGINEERING  ")
    assert len(matches) == 1
    assert matches[0]["company"] == "Google DeepMind"


def test_requirements_still_match_after_normalization():
    assert len(fetch_vetted_jobs("   high-performance  computing ")) == 1
