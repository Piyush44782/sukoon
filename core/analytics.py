"""Self-reported wellness analytics (trend + weekly comparison). Not a diagnostic tool."""
import numpy as np
from datetime import datetime

FIELDS = ("mood", "stress", "sleep", "overwhelmed", "connected")

def _vals(rows, f):
    return [(r["created_at"], r[f]) for r in rows if r.get(f) is not None]

def slope(values) -> float:
    """Least-squares slope per check-in (simple trend model)."""
    return float(np.polyfit(range(len(values)), values, 1)[0]) if len(values) >= 3 else 0.0

def weekly_means(rows, f) -> dict:
    out = {}
    for ts, v in _vals(rows, f):
        d = datetime.fromisoformat(ts)
        out.setdefault(f"{d.isocalendar()[0]}-W{d.isocalendar()[1]:02d}", []).append(v)
    return {k: round(float(np.mean(v)), 2) for k, v in sorted(out.items())}

def observations(rows) -> list[str]:
    """Gentle, personal, self-reported observations."""
    obs = []
    if len(rows) < 3:
        return ["Complete a few more check-ins to see patterns. There's no pressure or schedule to keep."]
    for f, label, bad_up in (("stress", "stress", True), ("mood", "mood", False)):
        v = [x for _, x in _vals(rows, f)]
        s = slope(v)
        if abs(s) >= 0.15:
            up = s > 0
            obs.append(f"Your self-reported {label} has {'increased' if up else 'decreased'} across recent check-ins.")
    sleep = [x for _, x in _vals(rows[-6:], "sleep")]
    if sum(1 for x in sleep if x <= 2) >= 2:
        obs.append("You've reported poor sleep several times recently.")
    w = weekly_means(rows, "stress")
    if len(w) >= 2:
        (a, b) = list(w.values())[-2:]
        obs.append(f"Average stress: {b} this week vs {a} last week (1 = low, 5 = high).")
    conn = [x for _, x in _vals(rows[-4:], "connected")]
    if conn and np.mean(conn) <= 2:
        obs.append("You've felt less socially connected lately. Reaching out to someone might help.")
    if any("stress" in o or "sleep" in o for o in obs):
        obs.append("Would you like to explore some stress-management activities? See Wellness Resources.")
    return obs or ["Your recent check-ins look fairly steady."]
