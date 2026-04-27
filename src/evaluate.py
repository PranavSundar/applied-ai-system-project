from dataclasses import dataclass
from typing import List

from .main import recommend_for_user


@dataclass
class EvalCase:
    genre: str
    mood: str
    energy: float
    expected_genre: str


def run_reliability_check() -> str:
    cases: List[EvalCase] = [
        EvalCase("electronic", "focused", 0.8, "electronic"),
        EvalCase("jazz", "calm", 0.3, "jazz"),
        EvalCase("hiphop", "hyped", 0.9, "hiphop"),
        EvalCase("indie", "dreamy", 0.5, "indie"),
        EvalCase("pop", "joyful", 0.65, "pop"),
        EvalCase("rock", "hyped", 0.85, "rock"),
    ]

    passed = 0
    conf_sum = 0.0
    for case in cases:
        out = recommend_for_user(case.genre, case.mood, case.energy, top_k=1)
        top = out[0]
        if top.song.genre == case.expected_genre:
            passed += 1
        conf_sum += top.confidence

    avg_conf = conf_sum / len(cases)
    return f"{passed} out of {len(cases)} checks passed; average confidence = {avg_conf:.2f}"
