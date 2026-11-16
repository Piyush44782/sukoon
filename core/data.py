"""All database operations. Student-owned records are always filtered by owner id."""
from datetime import datetime, timedelta
from core.database import get_conn
from core.crypto import encrypt, decrypt
import config

def q(sql, a=(), one=False):
    with get_conn() as c:
        r = c.execute(sql, a).fetchall()
    return (dict(r[0]) if r else None) if one else [dict(x) for x in r]

def ex(sql, a=()):
    with get_conn() as c:
        return c.execute(sql, a).lastrowid

# ---- profile ----
def get_profile(uid):
    return q("SELECT u.id,u.full_name,u.email,s.course,s.academic_year,s.semester FROM users u "
             "JOIN student_profiles s ON s.user_id=u.id WHERE u.id=?", (uid,), one=True)
def update_profile(uid, name, course, year, sem):
    ex("UPDATE users SET full_name=? WHERE id=?", (name.strip(), uid))
    ex("UPDATE student_profiles SET course=?,academic_year=?,semester=? WHERE user_id=?", (course, year, sem, uid))

# ---- conversations ----
def new_conversation(sid, title="New chat"):
    return ex("INSERT INTO conversations(student_id,title) VALUES(?,?)", (sid, title))
def list_conversations(sid):
    return q("SELECT * FROM conversations WHERE student_id=? ORDER BY id DESC", (sid,))
def rename_conversation(cid, sid, title):
    ex("UPDATE conversations SET title=? WHERE id=? AND student_id=?", (title[:40], cid, sid))
def get_messages(cid, sid):
    rows = q("SELECT m.* FROM messages m JOIN conversations c ON c.id=m.conversation_id "
             "WHERE c.id=? AND c.student_id=? ORDER BY m.id", (cid, sid))
    for r in rows: r["text"] = decrypt(r["content_enc"])
    return rows
def add_message(cid, sid, sender, text, sentiment=None, topics=None):
    if not q("SELECT 1 FROM conversations WHERE id=? AND student_id=?", (cid, sid)):
        raise PermissionError("Not your conversation.")
    ex("INSERT INTO messages(conversation_id,sender,content_enc,sentiment,topics) VALUES(?,?,?,?,?)",
       (cid, sender, encrypt(text), sentiment, ",".join(topics or [])))
def delete_conversation(cid, sid):
    ex("DELETE FROM conversations WHERE id=? AND student_id=?", (cid, sid))
def chat_stats(sid):
    return q("SELECT m.sentiment,m.topics FROM messages m JOIN conversations c ON c.id=m.conversation_id "
             "WHERE c.student_id=? AND m.sender='student'", (sid,))

# ---- journal ----
def add_journal(sid, date, cat, title, body):
    return ex("INSERT INTO journal_entries(student_id,entry_date,category,title,body_enc) VALUES(?,?,?,?,?)",
              (sid, str(date), cat, title, encrypt(body)))
def update_journal(eid, sid, date, cat, title, body):
    ex("UPDATE journal_entries SET entry_date=?,category=?,title=?,body_enc=? WHERE id=? AND student_id=?",
       (str(date), cat, title, encrypt(body), eid, sid))
def delete_journal(eid, sid):
    ex("DELETE FROM journal_entries WHERE id=? AND student_id=?", (eid, sid))
def list_journal(sid, search=""):
    rows = q("SELECT * FROM journal_entries WHERE student_id=? ORDER BY entry_date DESC,id DESC", (sid,))
    for r in rows: r["body"] = decrypt(r["body_enc"])
    s = search.strip().lower()
    return [r for r in rows if s in (r["title"] or "").lower() or s in r["body"].lower()] if s else rows

# ---- check-ins & prefs ----
def add_checkin(sid, mood, stress=None, sleep=None, overwhelmed=None, connected=None, note=""):
    ex("INSERT INTO checkins(student_id,mood,stress,sleep,overwhelmed,connected,note_enc) VALUES(?,?,?,?,?,?,?)",
       (sid, mood, stress, sleep, overwhelmed, connected, encrypt(note) if note else None))
def list_checkins(sid, days=60):
    rows = q("SELECT * FROM checkins WHERE student_id=? AND created_at>=datetime('now',?) ORDER BY id",
             (sid, f"-{days} days"))
    for r in rows: r["note"] = decrypt(r["note_enc"]) if r["note_enc"] else ""
    return rows
def get_prefs(sid):
    return q("SELECT * FROM notification_prefs WHERE student_id=?", (sid,), one=True) or \
        {"reminders_enabled": 1, "paused_until": None, "days": "Mon,Thu"}
def set_prefs(sid, enabled, paused_until, days):
    ex("INSERT OR REPLACE INTO notification_prefs VALUES(?,?,?,?)", (sid, int(enabled), paused_until, days))

# ---- parent consent ----
KINDS = {"involve": ["General wellness update", "Specific concern", "Journal entry", "Request for support"],
         "selected": ["Specific concern", "Journal entry", "Request for support"]}
def current_consent(sid):
    return q("SELECT * FROM consent_records WHERE student_id=? AND revoked_at IS NULL ORDER BY id DESC LIMIT 1",
             (sid,), one=True)
def revoke_consent(sid):
    ex("UPDATE consent_records SET revoked_at=CURRENT_TIMESTAMP WHERE student_id=? AND revoked_at IS NULL", (sid,))
def set_consent(sid, level, pname="", pcontact=""):
    revoke_consent(sid)
    return ex("INSERT INTO consent_records(student_id,parent_name,parent_contact,level) VALUES(?,?,?,?)",
              (sid, pname, pcontact, level))
def share_info(sid, kind, text):
    c = current_consent(sid)
    if not c or kind not in KINDS.get(c["level"], []):
        raise PermissionError("No active consent covers this kind of sharing.")
    return ex("INSERT INTO shared_information(consent_id,kind,content_enc) VALUES(?,?,?)", (c["id"], kind, encrypt(text)))
def shared_history(sid):
    rows = q("SELECT s.*,c.parent_name,c.revoked_at FROM shared_information s JOIN consent_records c "
             "ON c.id=s.consent_id WHERE c.student_id=? ORDER BY s.id DESC", (sid,))
    for r in rows: r["text"] = decrypt(r["content_enc"])
    return rows

# ---- providers & appointments ----
def list_providers(ptype):
    return q("SELECT u.id,u.full_name,u.is_demo,p.* FROM users u JOIN provider_profiles p ON p.user_id=u.id "
             "WHERE u.is_approved=1 AND u.is_active=1 AND p.provider_type=?", (ptype,))
def open_slots(pid):
    return q("SELECT * FROM availability_slots WHERE provider_id=? AND is_booked=0 AND slot_start>? "
             "ORDER BY slot_start", (pid, datetime.now().isoformat()))
def add_slot(pid, dt):
    ex("INSERT INTO availability_slots(provider_id,slot_start) VALUES(?,?)", (pid, dt.isoformat()))
def update_provider_profile(pid, desig, expertise, intro):
    ex("UPDATE provider_profiles SET designation=?,expertise=?,intro=? WHERE user_id=?", (desig, expertise, intro, pid))
def request_appointment(sid, pid, slot_id, note=""):
    with get_conn() as c:
        if not c.execute("SELECT 1 FROM availability_slots WHERE id=? AND provider_id=? AND is_booked=0",
                         (slot_id, pid)).fetchone():
            raise ValueError("That slot is no longer available.")
        c.execute("UPDATE availability_slots SET is_booked=1 WHERE id=?", (slot_id,))
        return c.execute("INSERT INTO appointments(student_id,provider_id,slot_id,note_enc) VALUES(?,?,?,?)",
                         (sid, pid, slot_id, encrypt(note) if note else None)).lastrowid
def appointments_for(uid, role):
    col, other = ("student_id", "provider_id") if role == "student" else ("provider_id", "student_id")
    rows = q(f"SELECT a.*,s.slot_start,u.full_name AS other_name FROM appointments a "
             f"LEFT JOIN availability_slots s ON s.id=a.slot_id JOIN users u ON u.id=a.{other} "
             f"WHERE a.{col}=? ORDER BY s.slot_start DESC", (uid,))
    for r in rows: r["note"] = decrypt(r["note_enc"]) if r["note_enc"] else ""
    return rows
def set_status(appt_id, uid, role, status):
    a = q("SELECT * FROM appointments WHERE id=?", (appt_id,), one=True)
    if not a: raise ValueError("Appointment not found.")
    if role == "student":
        ok = a["student_id"] == uid and status == "cancelled" and a["status"] in ("pending", "accepted")
    else:
        ok = a["provider_id"] == uid and ((status in ("accepted", "rejected") and a["status"] == "pending")
                                          or (status == "completed" and a["status"] == "accepted"))
    if not ok: raise PermissionError("Action not permitted.")
    ex("UPDATE appointments SET status=? WHERE id=?", (status, appt_id))
    if status in ("cancelled", "rejected") and a["slot_id"]:
        ex("UPDATE availability_slots SET is_booked=0 WHERE id=?", (a["slot_id"],))
def appt_messages(appt_id, uid):
    a = q("SELECT * FROM appointments WHERE id=? AND (student_id=? OR provider_id=?)", (appt_id, uid, uid), one=True)
    if not a: raise PermissionError("Not your appointment.")
    rows = q("SELECT m.*,u.full_name FROM appointment_messages m JOIN users u ON u.id=m.sender_id "
             "WHERE appointment_id=? ORDER BY m.id", (appt_id,))
    for r in rows: r["text"] = decrypt(r["content_enc"])
    return rows
def post_appt_message(appt_id, uid, text):
    appt_messages(appt_id, uid)   # authorisation check
    ex("INSERT INTO appointment_messages(appointment_id,sender_id,content_enc) VALUES(?,?,?)",
       (appt_id, uid, encrypt(text)))

# ---- resources ----
def list_resources(category=None):
    if category: return q("SELECT * FROM resources WHERE category=? ORDER BY id", (category,))
    return q("SELECT * FROM resources ORDER BY category,id")
def add_resource(cat, title, body, tags): ex("INSERT INTO resources(category,title,body,tags) VALUES(?,?,?,?)", (cat, title, body, tags))
def delete_resource(rid): ex("DELETE FROM resources WHERE id=?", (rid,))
def resources_for_topics(topics, limit=3):
    out = []
    for r in list_resources():
        if set((r["tags"] or "").split(",")) & set(topics): out.append(r)
    return out[:limit]

# ---- privacy: deletion ----
def delete_my_data(sid, what):
    tables = {"conversations": "DELETE FROM conversations WHERE student_id=?",
              "journal": "DELETE FROM journal_entries WHERE student_id=?",
              "checkins": "DELETE FROM checkins WHERE student_id=?"}
    ex(tables[what], (sid,))
def delete_account(sid): ex("DELETE FROM users WHERE id=? AND role='student'", (sid,))

# ---- admin (no access to private content) ----
def students_list():
    return q("SELECT u.id,u.full_name,u.email,u.is_active,u.is_demo,s.course,s.academic_year FROM users u "
             "JOIN student_profiles s ON s.user_id=u.id ORDER BY u.id")
def set_active(uid, active): ex("UPDATE users SET is_active=? WHERE id=? AND role='student'", (int(active), uid))
def pending_providers():
    return q("SELECT u.id,u.full_name,u.email,p.provider_type,p.designation,p.expertise FROM users u "
             "JOIN provider_profiles p ON p.user_id=u.id WHERE u.is_approved=0")
def approve_provider(uid): ex("UPDATE users SET is_approved=1 WHERE id=?", (uid,))
def reject_provider(uid): ex("DELETE FROM users WHERE id=? AND is_approved=0", (uid,))
def appointment_counts(): return q("SELECT status,COUNT(*) AS n FROM appointments GROUP BY status")
def aggregate_stats():
    n = q("SELECT COUNT(*) AS n FROM users WHERE role='student'", one=True)["n"]
    out = {"students": n, "checkins_7d": q("SELECT COUNT(*) AS n FROM checkins WHERE created_at>=datetime('now','-7 days')", one=True)["n"],
           "avg_mood": None, "topics": {}}
    k = config.MIN_AGGREGATE_GROUP
    r = q("SELECT AVG(mood) AS m,COUNT(DISTINCT student_id) AS d FROM checkins WHERE created_at>=datetime('now','-30 days')", one=True)
    if r["d"] >= k and r["m"] is not None: out["avg_mood"] = round(r["m"], 2)
    if n >= k:
        counts = {}
        for m in q("SELECT topics FROM messages WHERE sender='student' AND topics!=''"):
            for t in m["topics"].split(","): counts[t] = counts.get(t, 0) + 1
        out["topics"] = {t: c for t, c in counts.items() if c >= k}
    return out
def get_setting(k, default=""):
    r = q("SELECT value FROM settings WHERE key=?", (k,), one=True); return r["value"] if r else default
def set_setting(k, v): ex("INSERT OR REPLACE INTO settings VALUES(?,?)", (k, v))
