"""Wrapped text from PDF extraction should still match requirement phrases."""
from scoring import compute_dynamic_match


def test_wrapped_profile_phrase_matches_contiguous_requirement():
    score, matched, missing = compute_dynamic_match(
        ["Strong mathematical foundation", "Python"],
        "STRONG\n  MATHEMATICAL\tFOUNDATION; Python",
    )
    assert (score, matched, missing) == (
        100, ["Strong mathematical foundation", "Python"], []
    )


def test_duplicate_requirement_whitespace_is_normalized():
    score, matched, missing = compute_dynamic_match(
        ["Strong  mathematical foundation", "Strong\nmathematical foundation"],
        "strong mathematical foundation",
    )
    assert (score, matched, missing) == (100, ["Strong mathematical foundation"], [])
