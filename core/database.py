"""SQLite schema and connection helper."""
import sqlite3
from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('student','counsellor','mentor','admin')),
  is_active INTEGER NOT NULL DEFAULT 1,
  is_approved INTEGER NOT NULL DEFAULT 1,
  is_demo INTEGER NOT NULL DEFAULT 0,
  failed_logins INTEGER NOT NULL DEFAULT 0,
  locked_until TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS student_profiles(
  user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  course TEXT, academic_year INTEGER, semester INTEGER);
CREATE TABLE IF NOT EXISTS provider_profiles(
  user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  provider_type TEXT NOT NULL, designation TEXT, expertise TEXT, intro TEXT);
CREATE TABLE IF NOT EXISTS availability_slots(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  slot_start TEXT NOT NULL, is_booked INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS appointments(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider_id INTEGER NOT NULL REFERENCES users(id),
  slot_id INTEGER REFERENCES availability_slots(id),
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK(status IN ('pending','accepted','rejected','cancelled','completed')),
  note_enc TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS conversations(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS messages(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  sender TEXT NOT NULL CHECK(sender IN ('student','ai')),
  content_enc TEXT NOT NULL, sentiment TEXT, topics TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS journal_entries(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  entry_date TEXT NOT NULL, category TEXT, title TEXT, body_enc TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS checkins(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  mood INTEGER, stress INTEGER, sleep INTEGER, overwhelmed INTEGER, connected INTEGER,
  note_enc TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS notification_prefs(
  student_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  reminders_enabled INTEGER NOT NULL DEFAULT 1, paused_until TEXT,
  days TEXT NOT NULL DEFAULT 'Mon,Thu');
CREATE TABLE IF NOT EXISTS consent_records(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  parent_name TEXT, parent_contact TEXT,
  level TEXT NOT NULL CHECK(level IN ('involve','selected','none')),
  granted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, revoked_at TEXT);
CREATE TABLE IF NOT EXISTS shared_information(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  consent_id INTEGER NOT NULL REFERENCES consent_records(id) ON DELETE CASCADE,
  kind TEXT NOT NULL, content_enc TEXT NOT NULL,
  shared_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS resources(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL, tags TEXT);
CREATE TABLE IF NOT EXISTS appointment_messages(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  appointment_id INTEGER NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
  sender_id INTEGER NOT NULL, content_enc TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS audit_log(
  id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, action TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
"""

def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db() -> None:
    with get_conn() as c:
        c.executescript(SCHEMA)
