"""Missing optional profile fields must not fabricate the keyword 'None'."""
from scoring import build_profile_text, compute_dynamic_match


def test_missing_fields_are_empty_not_literal_none():
    profile = build_profile_text(None, None)
    assert profile.strip() == ""
    assert compute_dynamic_match(["none"], profile)[0] == 0


def test_provided_evidence_survives_missing_other_field():
    assert compute_dynamic_match(["Python"], build_profile_text(None, "Python"))[0] == 100
