"""Deterministic keyword coverage, not a hiring prediction."""
import re
import unicodedata


def _normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def compute_dynamic_match(requirements: list, profile_text: str, default_score: int = 0) -> tuple:
    requirements = list({_normalize(req.strip()): req.strip() for req in requirements if isinstance(req, str) and req.strip()}.values())
    profile_text = _normalize(profile_text)
    if not profile_text.strip():
        return 0, [], requirements
    matched, missing = [], []
    for req in requirements:
        # + and # distinguish C, C++, and C# rather than word suffixes.
        pattern = r"(?<![\w+#])" + re.escape(_normalize(req)) + r"(?![\w+#])"
        (matched if re.search(pattern, profile_text) else missing).append(req)
    if not requirements:
        return 0, [], []
    return round(100 * len(matched) / len(requirements)), matched, missing


def build_profile_text(skills: str, resume: str) -> str:
    """Only supplied skill evidence and resume text participate in scoring."""
    return f"{skills}\n{resume}"

