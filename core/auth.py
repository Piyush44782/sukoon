"""Authentication, password hashing, lockout and role-based access control."""
import hashlib, hmac, os, re
from datetime import datetime, timedelta
import config
from core.database import get_conn

class AuthError(Exception):
    """Raised with a user-safe message."""

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, config.PBKDF2_ITERATIONS)
    return f"{config.PBKDF2_ITERATIONS}${salt.hex()}${dk.hex()}"

def verify_password(password: str, stored: str) -> bool:
    try:
        iters, salt, dk = stored.split("$")
        new = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(iters))
        return hmac.compare_digest(new.hex(), dk)
    except ValueError:
        return False

def validate_password(pw: str) -> None:
    if (len(pw) < config.MIN_PASSWORD_LEN or not re.search(r"[A-Za-z]", pw)
            or not re.search(r"\d", pw)):
        raise AuthError(f"Password needs {config.MIN_PASSWORD_LEN}+ characters with letters and numbers.")

def validate_email(email: str) -> str:
    email = email.strip().lower()
    if not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", email):
        raise AuthError("Please enter a valid email address.")
    if not email.endswith("@" + config.ALLOWED_EMAIL_DOMAIN):
        raise AuthError(f"SUKOON is only for VIPS students. Use your @{config.ALLOWED_EMAIL_DOMAIN} email.")
    return email

def _audit(user_id, action):
    with get_conn() as c:
        c.execute("INSERT INTO audit_log(user_id, action) VALUES(?,?)", (user_id, action))

def register_student(full_name, email, password, course, academic_year, semester) -> int:
    full_name = full_name.strip()
    if len(full_name) < 2:
        raise AuthError("Please enter your full name.")
    email = validate_email(email)
    validate_password(password)
    if course not in config.COURSES or not (1 <= int(academic_year) <= 5) or not (1 <= int(semester) <= 10):
        raise AuthError("Please check your course, year and semester.")
    with get_conn() as c:
        if c.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            raise AuthError("An account with this email already exists.")
        uid = c.execute(
            "INSERT INTO users(full_name,email,password_hash,role) VALUES(?,?,?,'student')",
            (full_name, email, hash_password(password))).lastrowid
        c.execute("INSERT INTO student_profiles VALUES(?,?,?,?)", (uid, course, academic_year, semester))
        c.execute("INSERT INTO notification_prefs(student_id) VALUES(?)", (uid,))
    _audit(uid, "register")
    return uid

def login(email: str, password: str) -> dict:
    """Return the user row as dict, or raise AuthError (same message for bad email/password)."""
    email = email.strip().lower()
    with get_conn() as c:
        u = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if not u:
            raise AuthError("Incorrect email or password.")
        if u["locked_until"] and datetime.fromisoformat(u["locked_until"]) > datetime.utcnow():
            raise AuthError("Too many attempts. Please try again in a few minutes.")
        if not verify_password(password, u["password_hash"]):
            n = u["failed_logins"] + 1
            lock = None
            if n >= config.MAX_FAILED_LOGINS:
                lock = (datetime.utcnow() + timedelta(minutes=config.LOCKOUT_MINUTES)).isoformat()
                n = 0
            c.execute("UPDATE users SET failed_logins=?, locked_until=? WHERE id=?", (n, lock, u["id"]))
            c.commit()
            raise AuthError("Incorrect email or password.")
        if not u["is_active"]:
            raise AuthError("This account is deactivated. Please contact the administrator.")
        if not u["is_approved"]:
            raise AuthError("Your account is awaiting administrator approval.")
        c.execute("UPDATE users SET failed_logins=0, locked_until=NULL WHERE id=?", (u["id"],))
    _audit(u["id"], "login")
    return {k: u[k] for k in ("id", "full_name", "email", "role", "is_demo")}

def change_password(user_id: int, old: str, new: str) -> None:
    validate_password(new)
    with get_conn() as c:
        u = c.execute("SELECT password_hash FROM users WHERE id=?", (user_id,)).fetchone()
        if not u or not verify_password(old, u["password_hash"]):
            raise AuthError("Current password is incorrect.")
        c.execute("UPDATE users SET password_hash=? WHERE id=?", (hash_password(new), user_id))
    _audit(user_id, "change_password")

def has_role(user, *roles: str) -> bool:
    return bool(user) and user["role"] in roles

def require_role(user, *roles: str) -> None:
    if not has_role(user, *roles):
        raise PermissionError("You do not have access to this area.")

def register_provider(full_name, email, password, provider_type, designation, expertise, intro) -> int:
    """Counsellor/mentor sign-up. Account stays unapproved until an admin approves it."""
    if provider_type not in config.PROVIDER_TYPES:
        raise AuthError("Please choose a valid provider type.")
    email = validate_email(email); validate_password(password)
    if len(full_name.strip()) < 2: raise AuthError("Please enter your full name.")
    role = "counsellor" if provider_type == "College Counsellor" else "mentor"
    with get_conn() as c:
        if c.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            raise AuthError("An account with this email already exists.")
        uid = c.execute("INSERT INTO users(full_name,email,password_hash,role,is_approved) VALUES(?,?,?,?,0)",
                        (full_name.strip(), email, hash_password(password), role)).lastrowid
        c.execute("INSERT INTO provider_profiles VALUES(?,?,?,?,?)",
                  (uid, provider_type, designation, expertise, intro))
    return uid
