from src.main import recommend_for_user
from src.reliability import validate_request


def test_valid_request_passes():
    ok, _ = validate_request("electronic", "focused", 0.8)
    assert ok is True


def test_invalid_request_rejected():
    ok, msg = validate_request("metal", "focused", 0.8)
    assert ok is False
    assert "Unsupported genre" in msg


def test_recommendation_returns_results():
    recs = recommend_for_user("jazz", "calm", 0.3, top_k=3)
    assert len(recs) >= 1
    assert recs[0].song.genre in {"jazz", "indie", "folk", "classical", "pop", "electronic", "hiphop", "rock"}


def test_confidence_in_range():
    recs = recommend_for_user("hiphop", "hyped", 0.9, top_k=2)
    assert 0.0 <= recs[0].confidence <= 1.0
