"""Field-level encryption (Fernet) for sensitive text such as journals and chats."""
from cryptography.fernet import Fernet
from config import KEY_PATH

def _key() -> bytes:
    if not KEY_PATH.exists():
        KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        KEY_PATH.write_bytes(Fernet.generate_key())
        try: KEY_PATH.chmod(0o600)
        except OSError: pass
    return KEY_PATH.read_bytes()

_f = Fernet(_key())

def encrypt(text: str) -> str:
    return _f.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    return _f.decrypt(token.encode()).decode()
