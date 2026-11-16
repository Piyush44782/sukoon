"""Starter wellness resources (general guidance; not medical advice)."""
from core import data
from core.safety import helpline_text

R = [("Breathing", "Box breathing (2 min)", "Breathe in for 4 seconds, hold for 4, breathe out for 4, hold for 4. Repeat 6-8 rounds. Keep shoulders relaxed.", "academic,distress,general"),
 ("Breathing", "Slow exhale breathing", "Inhale gently for 4 seconds, exhale slowly for 6-8 seconds. Do this for 2-3 minutes before an exam or difficult conversation.", "academic,distress"),
 ("Meditation", "5-minute body scan", "Sit or lie comfortably. Bring attention slowly from your toes to your head, noticing sensations without trying to change them. If your mind wanders, gently return.", "distress,isolation,general"),
 ("Relaxation", "5-4-3-2-1 grounding", "Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste. It helps anchor you when thoughts race.", "distress,academic"),
 ("Stress management", "Break the task down", "Write the one next small step for the thing that feels huge. Work 25 minutes, rest 5. Celebrate finishing, not perfection.", "academic,career,general"),
 ("Study-life balance", "Protect your basics", "Aim for regular sleep, meals and a little movement daily. A short walk and one non-study activity each day help focus more than extra late-night hours.", "academic,general"),
 ("Academic pressure", "When results feel like your worth", "Marks measure one slice of learning, not your value. List what you can control this week (revision, sleep, asking a teacher) and let the rest go. Talking to a faculty mentor can help.", "academic,family"),
 ("Connection", "Reaching out when you feel alone", "Send one low-pressure message to someone (\"free for chai?\"). Small, regular contact matters more than big gestures. Peer mentors and counsellors are available in Talk to Someone.", "isolation,relationship"),
 ("Career", "Feeling unsure about your career", "Uncertainty is normal. Try one small experiment: talk to a senior, try a short course, or attend a placement-cell session. A faculty mentor can help you map options.", "career"),
 ("Family", "When expectations feel heavy", "Try one calm conversation: say what you appreciate, what feels hard, and one thing you need. SUKOON's Parent Inclusion section lets you share only what you choose.", "family"),
 ("Helplines", "Verified helplines (India)", helpline_text() + "\n\nPlease verify numbers with official sources. If you are in immediate danger, call 112.", "distress,crisis")]

def seed_resources():
    if not data.list_resources():
        for r in R: data.add_resource(*r)
