from dataclasses import dataclass
from typing import List, Tuple

from .models import Song, UserProfile


@dataclass
class Recommendation:
    song: Song
    score: float
    confidence: float
    explanation: str


def _score_song(song: Song, user: UserProfile) -> Tuple[float, str]:
    score = 0.0
    reasons: List[str] = []

    if song.genre == user.preferred_genre.lower():
        score += 0.45
        reasons.append("genre match")
    if song.mood == user.preferred_mood.lower():
        score += 0.30
        reasons.append("mood match")

    energy_gap = abs(song.energy - user.target_energy)
    energy_score = max(0.0, 0.25 - (energy_gap * 0.5))
    score += energy_score
    reasons.append(f"energy gap {energy_gap:.2f}")

    tempo_gap = abs(song.tempo - int(user.target_energy * 140))
    if tempo_gap <= user.max_tempo_delta:
        score += 0.10
        reasons.append("tempo in range")

    explanation = ", ".join(reasons)
    return min(score, 1.0), explanation


def rank_recommendations(candidates: List[Song], user: UserProfile, top_k: int = 3) -> List[Recommendation]:
    scored: List[Recommendation] = []
    for song in candidates:
        score, explanation = _score_song(song, user)
        confidence = max(0.2, min(0.99, score))
        scored.append(
            Recommendation(song=song, score=round(score, 3), confidence=round(confidence, 3), explanation=explanation)
        )

    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:top_k]
