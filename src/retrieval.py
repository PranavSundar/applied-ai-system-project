import csv
import logging
from pathlib import Path
from typing import List

from .models import Song


LOGGER = logging.getLogger(__name__)


def load_songs(csv_path: str) -> List[Song]:
    songs: List[Song] = []
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Song catalog not found: {csv_path}")

    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            songs.append(
                Song(
                    title=row["title"].strip(),
                    artist=row["artist"].strip(),
                    genre=row["genre"].strip().lower(),
                    mood=row["mood"].strip().lower(),
                    energy=float(row["energy"]),
                    tempo=int(row["tempo"]),
                )
            )

    LOGGER.info("Loaded %s songs from catalog", len(songs))
    return songs


def retrieve_candidates(
    songs: List[Song], genre: str, mood: str, tempo_anchor: int, max_tempo_delta: int = 35
) -> List[Song]:
    """
    Lightweight RAG-style retrieval step:
    filter the global catalog into a focused context window
    before ranking/generation.
    """
    genre = genre.lower().strip()
    mood = mood.lower().strip()

    exact_matches = [
        s
        for s in songs
        if s.genre == genre and s.mood == mood and abs(s.tempo - tempo_anchor) <= max_tempo_delta
    ]
    if exact_matches:
        LOGGER.info("Retriever found %s exact context songs", len(exact_matches))
        return exact_matches

    relaxed_matches = [
        s for s in songs if (s.genre == genre or s.mood == mood) and abs(s.tempo - tempo_anchor) <= 45
    ]
    LOGGER.info("Retriever found %s relaxed context songs", len(relaxed_matches))
    return relaxed_matches if relaxed_matches else songs
