"""Central configuration for SUKOON (VIPS Pitampura only)."""
from pathlib import Path

APP_NAME = "SUKOON"
TAGLINE = "A safe space. A listening ear. A better tomorrow."
DB_PATH = Path(__file__).parent / "data" / "sukoon.db"
KEY_PATH = Path(__file__).parent / "data" / "secret.key"   # Fernet key; never commit
# VIPS-only: registration is restricted to this email domain. Change if your
# college uses a different domain.
ALLOWED_EMAIL_DOMAIN = "vips.edu"
ROLES = ("student", "counsellor", "mentor", "admin")
PROVIDER_TYPES = ("College Counsellor", "Faculty Mentor", "Trained Peer Mentor")
COURSES = ("BCA", "BBA", "BA (JMC)", "BA LLB", "BBA LLB", "B.Ed", "MCA", "MBA", "Other")
PBKDF2_ITERATIONS = 310_000
MAX_FAILED_LOGINS = 5
LOCKOUT_MINUTES = 10
MIN_PASSWORD_LEN = 8
import os
AI_MODEL = os.environ.get("SUKOON_MODEL", "claude-sonnet-5-5")
MIN_AGGREGATE_GROUP = 5   # admin stats hidden below this many students (anonymity)

# ---- AI provider: "groq" (free, default) | "ollama" (local, private) | "anthropic" ----
AI_PROVIDER = os.environ.get("SUKOON_AI_PROVIDER", "groq").lower()
GROQ_MODEL = os.environ.get("SUKOON_GROQ_MODEL", "openai/gpt-oss-120b")
OLLAMA_MODEL = os.environ.get("SUKOON_OLLAMA_MODEL", "llama3.2")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/v1/chat/completions")
