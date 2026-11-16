"""Rule-based crisis detection (never relies on sentiment alone) and verified helplines.
VERIFY helpline numbers with VIPS/official sources before any real deployment."""
import re

CRISIS_PATTERNS = [r"\bkill(ing)? myself\b", r"\bsuicid", r"\bend(ing)? (my|this) life\b", r"\bwant(ed)? to die\b",
    r"\b(don'?t|do not) want to (live|be here|exist)\b", r"\bself[- ]?harm", r"\bcut(ting)? myself\b",
    r"\bhurt(ing)? myself\b", r"\bno reason to live\b", r"\bbetter off (dead|without me)\b",
    r"\bend it all\b", r"\bnot worth living\b", r"\btake my own life\b", r"\boverdose\b"]
HELPLINES = [("Emergency services (India)", "112"),
             ("Tele-MANAS, 24x7 free mental health support (Govt. of India)", "14416 or 1800-891-4416"),
             ("KIRAN Mental Health Helpline, 24x7 (Govt. of India)", "1800-599-0019")]
CONFIDENTIALITY_NOTE = ("SUKOON keeps your chats private by default. If you may be in immediate danger, "
    "we cannot promise absolute confidentiality: involving a trusted person, a counsellor or emergency "
    "services may become necessary to keep you safe.")

def detect_crisis(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in CRISIS_PATTERNS)

def helpline_text() -> str:
    return "\n".join(f"- **{n}**: {num}" for n, num in HELPLINES)

CRISIS_REPLY = ("I'm really glad you told me this, and I'm taking it seriously. What you're feeling sounds "
    "incredibly heavy, and you deserve support right now, not just from an app.\n\n"
    "**Please reach out to someone now:**\n" + helpline_text() +
    "\n\nIf you can, tell a person you trust (a friend, family member, or someone at college) so you "
    "are not alone with this. You can also use **Talk to Someone** in the menu to request a session with a "
    "VIPS counsellor.\n\nIf you are in immediate danger, please call 112. I'm still here, and I'd like to "
    "listen. Would you tell me what's been happening?\n\n_" + CONFIDENTIALITY_NOTE + "_")
