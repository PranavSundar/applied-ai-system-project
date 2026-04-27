from typing import List, Tuple

from .recommender import Recommendation


ALLOWED_MOODS = {"calm", "focused", "hyped", "dreamy", "joyful"}
ALLOWED_GENRES = {"pop", "electronic", "jazz", "rock", "indie", "classical", "hiphop", "folk"}


def validate_request(genre: str, mood: str, target_energy: float) -> Tuple[bool, str]:
    if genre.lower() not in ALLOWED_GENRES:
        return False, f"Unsupported genre '{genre}'. Allowed: {sorted(ALLOWED_GENRES)}"
    if mood.lower() not in ALLOWED_MOODS:
        return False, f"Unsupported mood '{mood}'. Allowed: {sorted(ALLOWED_MOODS)}"
    if not (0.0 <= target_energy <= 1.0):
        return False, "target_energy must be in [0.0, 1.0]"
    return True, "ok"


def enforce_output_guardrail(recs: List[Recommendation]) -> List[Recommendation]:
    """
    Keep recommendations that pass minimum quality threshold.
    This reduces clearly weak matches in low-context settings.
    """
    filtered = [r for r in recs if r.score >= 0.35]
    return filtered if filtered else recs[:1]
