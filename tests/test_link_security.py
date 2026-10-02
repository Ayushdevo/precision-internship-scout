"""Career links must not be interpreted differently by browsers and URL parsers."""
import pytest

from rendering import safe_careers_url


@pytest.mark.parametrize("candidate", [
    "https://example.com\\evil.com",
    "https://example.com/\\@attacker.example",
    "https://example.com/\x00path",
    "https://example.com/\x7fpath",
])
def test_unsafe_career_urls_are_rejected(candidate):
    assert safe_careers_url(candidate) is None


def test_normal_career_link_remains_usable():
    assert safe_careers_url("https://example.com/jobs?team=ml") == "https://example.com/jobs?team=ml"
