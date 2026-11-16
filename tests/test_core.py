import pytest
from core import database, auth, data, safety, nlp, analytics
from core.resources_seed import seed_resources

@pytest.fixture(autouse=True)
def tmpdb(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "t.db"); database.init_db()

def stu(email):
    return auth.register_student("Asha Rao", email, "Passw0rd1", "BCA", 2, 3)

def test_crisis_detection():
    assert safety.detect_crisis("I want to end my life")
    assert not safety.detect_crisis("exam stress is killing my vibe")

def test_nlp():
    a = nlp.analyze("I'm not happy, my parents expect too much and exams stress me")
    assert a["sentiment"] == "negative" and {"family", "academic"} <= set(a["topics"])

def test_analytics_trend():
    rows = [{"created_at": f"2026-11-{d:02d} 10:00:00", "stress": s, "mood": 3, "sleep": 2, "connected": 3, "overwhelmed": 3}
            for d, s in zip(range(1, 8), [1, 2, 2, 3, 4, 4, 5])]
    assert any("stress has increased" in o for o in analytics.observations(rows))

def test_conversation_isolation_and_encryption():
    a, b = stu("a@vips.edu"), stu("b@vips.edu")
    cid = data.new_conversation(a); data.add_message(cid, a, "student", "secret")
    assert data.get_messages(cid, b) == []
    with pytest.raises(PermissionError): data.add_message(cid, b, "student", "x")
    assert "secret" not in data.q("SELECT content_enc FROM messages")[0]["content_enc"]

def test_consent_flow():
    a = stu("a@vips.edu")
    with pytest.raises(PermissionError): data.share_info(a, "Specific concern", "hi")
    data.set_consent(a, "selected", "Mr R", "123")
    with pytest.raises(PermissionError): data.share_info(a, "General wellness update", "hi")
    data.share_info(a, "Specific concern", "hi"); assert len(data.shared_history(a)) == 1
    data.revoke_consent(a)
    with pytest.raises(PermissionError): data.share_info(a, "Specific concern", "hi")

def test_appointment_rules():
    a, b = stu("a@vips.edu"), stu("b@vips.edu")
    p = auth.register_provider("Dr P", "p@vips.edu", "Passw0rd1", "College Counsellor", "d", "e", "i")
    data.approve_provider(p)
    from datetime import datetime, timedelta; data.add_slot(p, datetime.now() + timedelta(days=1))
    sl = data.open_slots(p)[0]["id"]; ap = data.request_appointment(a, p, sl)
    with pytest.raises(ValueError): data.request_appointment(b, p, sl)      # no double booking
    with pytest.raises(PermissionError): data.set_status(ap, b, "student", "cancelled")
    with pytest.raises(PermissionError): data.appt_messages(ap, b)
    data.set_status(ap, p, "counsellor", "rejected"); assert data.open_slots(p)

def test_admin_aggregates_hidden_when_small():
    stu("a@vips.edu"); assert data.aggregate_stats()["avg_mood"] is None

def test_resources_seed():
    seed_resources(); assert data.resources_for_topics(["academic"])

def test_groq_provider_parsing(monkeypatch):
    import io, json, urllib.request, config
    from core import ai
    monkeypatch.setenv("GROQ_API_KEY", "gsk_test"); monkeypatch.setattr(config, "AI_PROVIDER", "groq")
    class R(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *a): pass
    monkeypatch.setattr(urllib.request, "urlopen",
        lambda req, timeout=0: R(json.dumps({"choices": [{"message": {"content": " Hello there "}}]}).encode()))
    assert ai.reply([{"role": "user", "content": "hi"}]) == "Hello there"

def test_provider_failure_falls_back(monkeypatch):
    import urllib.request, config
    from core import ai
    monkeypatch.setenv("GROQ_API_KEY", "gsk_secret123"); monkeypatch.setattr(config, "AI_PROVIDER", "groq")
    def boom(*a, **k): raise OSError("net down gsk_secret123")
    monkeypatch.setattr(urllib.request, "urlopen", boom)
    assert ai.reply([{"role": "user", "content": "hi"}]) == ai.FALLBACK
    assert "gsk_secret123" not in ai.LAST_ERROR
