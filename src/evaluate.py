from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from .main import recommend_for_user
from .models import UserProfile
from .recommender import Recommendation, rank_recommendations
from .reliability import enforce_output_guardrail
from .retrieval import load_songs


@dataclass
class EvalCase:
    genre: str
    mood: str
    energy: float
    expected_genre: str


DEFAULT_EVAL_CASES: List[EvalCase] = [
    EvalCase("electronic", "focused", 0.8, "electronic"),
    EvalCase("jazz", "calm", 0.3, "jazz"),
    EvalCase("hiphop", "hyped", 0.9, "hiphop"),
    EvalCase("indie", "dreamy", 0.5, "indie"),
    EvalCase("pop", "joyful", 0.65, "pop"),
    EvalCase("rock", "hyped", 0.85, "rock"),
]
CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "songs.csv"


def _baseline_recommend_for_user(genre: str, mood: str, target_energy: float, top_k: int = 1) -> List[Recommendation]:
    """
    Baseline system: score the full catalog directly (no retrieval step).
    This gives a measurable reference point against the retrieval-aware system.
    """
    user = UserProfile(preferred_genre=genre, preferred_mood=mood, target_energy=target_energy)
    songs = load_songs(str(CATALOG_PATH))
    ranked = rank_recommendations(songs, user=user, top_k=top_k)
    return enforce_output_guardrail(ranked)


def _run_suite(cases: List[EvalCase], use_retrieval_system: bool) -> Tuple[int, float]:
    passed = 0
    confidence_sum = 0.0

    for case in cases:
        if use_retrieval_system:
            out = recommend_for_user(case.genre, case.mood, case.energy, top_k=1)
        else:
            out = _baseline_recommend_for_user(case.genre, case.mood, case.energy, top_k=1)

        top = out[0]
        if top.song.genre == case.expected_genre:
            passed += 1
        confidence_sum += top.confidence

    avg_confidence = confidence_sum / len(cases)
    return passed, avg_confidence


def run_detailed_evaluation(cases: List[EvalCase] = DEFAULT_EVAL_CASES) -> str:
    lines: List[str] = []
    lines.append("=== Reliability Harness Report ===")
    lines.append(f"Cases: {len(cases)}")
    lines.append("")

    retrieval_passed = 0
    retrieval_conf_sum = 0.0
    baseline_passed = 0
    baseline_conf_sum = 0.0

    for idx, case in enumerate(cases, start=1):
        retrieval_top = recommend_for_user(case.genre, case.mood, case.energy, top_k=1)[0]
        baseline_top = _baseline_recommend_for_user(case.genre, case.mood, case.energy, top_k=1)[0]

        retrieval_ok = retrieval_top.song.genre == case.expected_genre
        baseline_ok = baseline_top.song.genre == case.expected_genre

        if retrieval_ok:
            retrieval_passed += 1
        if baseline_ok:
            baseline_passed += 1

        retrieval_conf_sum += retrieval_top.confidence
        baseline_conf_sum += baseline_top.confidence

        lines.append(
            f"[{idx}] input=({case.genre}, {case.mood}, {case.energy:.2f}) expected={case.expected_genre}"
        )
        lines.append(
            f"  retrieval -> {retrieval_top.song.title} ({retrieval_top.song.genre}) "
            f"conf={retrieval_top.confidence:.2f} {'PASS' if retrieval_ok else 'FAIL'}"
        )
        lines.append(
            f"  baseline  -> {baseline_top.song.title} ({baseline_top.song.genre}) "
            f"conf={baseline_top.confidence:.2f} {'PASS' if baseline_ok else 'FAIL'}"
        )

    retrieval_avg_conf = retrieval_conf_sum / len(cases)
    baseline_avg_conf = baseline_conf_sum / len(cases)
    retrieval_rate = retrieval_passed / len(cases)
    baseline_rate = baseline_passed / len(cases)

    lines.append("")
    lines.append("=== Summary ===")
    lines.append(
        f"Retrieval-aware: {retrieval_passed}/{len(cases)} passed "
        f"({retrieval_rate:.1%}), avg confidence={retrieval_avg_conf:.2f}"
    )
    lines.append(
        f"Baseline:        {baseline_passed}/{len(cases)} passed "
        f"({baseline_rate:.1%}), avg confidence={baseline_avg_conf:.2f}"
    )
    lines.append(
        f"Delta: pass-rate {(retrieval_rate - baseline_rate):+.1%}, "
        f"confidence {(retrieval_avg_conf - baseline_avg_conf):+.2f}"
    )

    return "\n".join(lines)


def run_reliability_check() -> str:
    passed, avg_conf = _run_suite(DEFAULT_EVAL_CASES, use_retrieval_system=True)
    return f"{passed} out of {len(DEFAULT_EVAL_CASES)} checks passed; average confidence = {avg_conf:.2f}"


if __name__ == "__main__":
    print(run_detailed_evaluation())
