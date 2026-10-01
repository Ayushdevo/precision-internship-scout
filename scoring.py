"""Deterministic keyword coverage, not a hiring prediction."""
import re


def compute_dynamic_match(requirements: list, profile_text: str, default_score: int = 0) -> tuple:
    unique_requirements = []
    seen = set()
    for requirement in requirements:
        if not isinstance(requirement, str):
            continue
        label = requirement.strip()
        key = label.casefold()
        if label and key not in seen:
            seen.add(key)
            unique_requirements.append(label)
    requirements = unique_requirements
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


def build_profile_text(skills: str, resume: str) -> str:
    """Only supplied skill evidence and resume text participate in scoring."""
    return f"{skills}\n{resume}"
