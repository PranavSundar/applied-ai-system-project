import logging
from pathlib import Path
from typing import List

from .models import UserProfile
from .recommender import Recommendation, rank_recommendations
from .reliability import enforce_output_guardrail, validate_request
from .retrieval import load_songs, retrieve_candidates


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
LOGGER = logging.getLogger(__name__)


CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "songs.csv"


def recommend_for_user(genre: str, mood: str, target_energy: float, top_k: int = 3) -> List[Recommendation]:
    ok, message = validate_request(genre, mood, target_energy)
    if not ok:
        raise ValueError(message)

    user = UserProfile(preferred_genre=genre, preferred_mood=mood, target_energy=target_energy)
    songs = load_songs(str(CATALOG_PATH))
    tempo_anchor = int(target_energy * 140)

    # RAG-like step: retrieve a context set first, then rank.
    candidates = retrieve_candidates(songs, genre=genre, mood=mood, tempo_anchor=tempo_anchor)
    ranked = rank_recommendations(candidates, user=user, top_k=top_k)
    return enforce_output_guardrail(ranked)


def run_cli() -> None:
    print("=== Music Recommender AI (Project 4) ===")
    genre = input("Preferred genre: ").strip().lower()
    mood = input("Current mood (calm/focused/hyped/dreamy/joyful): ").strip().lower()
    energy = float(input("Target energy (0.0 - 1.0): ").strip())

    recs = recommend_for_user(genre, mood, energy, top_k=3)
    print("\nTop recommendations:")
    for idx, rec in enumerate(recs, start=1):
        print(
            f"{idx}. {rec.song.title} - {rec.song.artist} | "
            f"score={rec.score:.2f}, confidence={rec.confidence:.2f} | {rec.explanation}"
        )


if __name__ == "__main__":
    run_cli()
