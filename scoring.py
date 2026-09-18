"""Deterministic keyword coverage, not a hiring prediction."""
import re


def compute_dynamic_match(requirements: list, profile_text: str, default_score: int = 0) -> tuple:
    requirements = list({req.strip().casefold(): req.strip() for req in requirements if isinstance(req, str) and req.strip()}.values())
    profile_text = profile_text.casefold()
    if not profile_text.strip():
        return 0, [], requirements
    matched, missing = [], []
    for req in requirements:
        pattern = r"(?<!\w)" + re.escape(req.casefold()) + r"(?!\w)"
        (matched if re.search(pattern, profile_text) else missing).append(req)
    if not requirements:
        return 0, [], []
    return round(100 * len(matched) / len(requirements)), matched, missing
