from dataclasses import dataclass


@dataclass
class Song:
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo: int


@dataclass
class UserProfile:
    preferred_genre: str
    preferred_mood: str
    target_energy: float
    max_tempo_delta: int = 25
