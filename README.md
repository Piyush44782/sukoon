# SUKOON: AI Student Mental Wellness Platform (VIPS Pitampura)
*A safe space. A listening ear. A better tomorrow.*

## Setup
```
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."     # Windows: set ANTHROPIC_API_KEY=...  (or .streamlit/secrets.toml)
python seed.py
streamlit run app.py
python -m pytest                           # 16 automated tests
```
Set your college email domain in `config.py` (`ALLOWED_EMAIL_DOMAIN`). Model: env `SUKOON_MODEL`.

## Demo accounts (synthetic, NOT real VIPS staff; password `Demo@1234`)
student.demo@ / counsellor.demo@ / faculty.demo@ / peer.demo@ / admin.demo@ + your domain.

## Architecture
| File | Responsibility |
|---|---|
| `app.py` | Login, registration, role routing, theme |
| `views/student.py` `provider.py` `admin.py` | Frontend per role (10 student sections) |
| `core/auth.py` | PBKDF2 hashing, lockout, RBAC, validation |
| `core/data.py` | All DB operations; owner-filtered queries |
| `core/crypto.py` | Fernet encryption of chats, journals, notes |
| `core/ai.py` | Claude companion (system prompt forbids diagnosis/medication) + offline fallback |
| `core/nlp.py` | Lexicon sentiment (with negation), emotions, 6 concern topics |
| `core/safety.py` | Regex crisis rules (not sentiment-only), helplines, confidentiality limits |
| `core/analytics.py` | Least-squares trend (numpy), weekly means, personal observations |
| `core/scheduler.py` | Twice-weekly in-app reminders; honours pause/disable; missed != distress |

## AI / NLP / ML explanation
- **AI:** conversation history (last 20 turns) goes to the Anthropic API with a safety-focused system prompt.
- **NLP:** transparent word-lexicon approach, shown to students as imperfect signals.
- **ML:** linear-regression trends and week-over-week comparison on *self-reported* data. No illness prediction or labelling. Admin stats are aggregated with a minimum group size of 5.
- **Safety:** crisis rules run before the AI; a fixed supportive reply with verified helplines is used.

## Privacy notes
Chats/journals/check-in notes encrypted at rest; admins cannot query private content; parent sharing requires consent, per-item review, timestamps, history and revocation. Parents have no login: shared messages are downloaded by the student and sent by them.

## Before real deployment
Review by VIPS authorities and qualified mental health professionals; verify helpline numbers; use HTTPS; back up `data/secret.key` securely.
