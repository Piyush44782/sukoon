import pytest, config
from core import database, auth

@pytest.fixture(autouse=True)
def tmpdb(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "t.db")
    database.init_db()

def reg(email="a@vips.edu", pw="Passw0rd1"):
    return auth.register_student("Asha Rao", email, pw, "BCA", 2, 3)

def test_register_and_login():
    reg(); assert auth.login("a@vips.edu", "Passw0rd1")["role"] == "student"

def test_password_is_hashed():
    reg()
    with database.get_conn() as c:
        h = c.execute("SELECT password_hash FROM users").fetchone()[0]
    assert "Passw0rd1" not in h

def test_non_vips_email_rejected():
    with pytest.raises(auth.AuthError): reg("a@gmail.com")

def test_weak_password_rejected():
    with pytest.raises(auth.AuthError): reg(pw="short")

def test_duplicate_email_rejected():
    reg()
    with pytest.raises(auth.AuthError): reg()

def test_wrong_password_and_lockout():
    reg()
    for _ in range(config.MAX_FAILED_LOGINS):
        with pytest.raises(auth.AuthError): auth.login("a@vips.edu", "wrong")
    with pytest.raises(auth.AuthError, match="Too many"): auth.login("a@vips.edu", "Passw0rd1")

def test_rbac():
    with pytest.raises(PermissionError): auth.require_role({"role": "student"}, "admin")
    auth.require_role({"role": "student"}, "student")

def test_unapproved_provider_blocked():
    with database.get_conn() as c:
        c.execute("INSERT INTO users(full_name,email,password_hash,role,is_approved) VALUES('P','p@vips.edu',?, 'mentor',0)",
                  (auth.hash_password("Passw0rd1"),))
    with pytest.raises(auth.AuthError, match="approval"): auth.login("p@vips.edu", "Passw0rd1")
