"""Check-in reminder logic (twice-weekly cadence). In-app reminders: shown when a check-in is due.
Missed check-ins are never interpreted as distress."""
from datetime import datetime, timedelta
from core import data

def checkin_due(sid: int) -> bool:
    p = data.get_prefs(sid)
    if not p["reminders_enabled"]:
        return False
    if p["paused_until"] and datetime.fromisoformat(p["paused_until"]) > datetime.now():
        return False
    rows = data.list_checkins(sid, 14)
    if not rows:
        return True
    return datetime.utcnow() - datetime.fromisoformat(rows[-1]["created_at"]) >= timedelta(days=3)
