"""Deterministic keyword coverage, not a hiring prediction."""
import re


def normalize_requirements(requirements: list) -> list[str]:
    """Preserve the first nonempty label, ignoring case/spacing duplicates."""
    unique_requirements = []
    seen = set()
    for requirement in requirements:
        if not isinstance(requirement, str):
            continue
        label = " ".join(requirement.split())
        key = label.casefold()
        if label and key not in seen:
            seen.add(key)
            unique_requirements.append(label)
    return unique_requirements


def compute_dynamic_match(requirements: list, profile_text: str, default_score: int = 0) -> tuple:
    requirements = normalize_requirements(requirements)
    profile_text = re.sub(r"\s+", " ", profile_text).casefold()
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
    return f"{skills or ''}\n{resume or ''}"
