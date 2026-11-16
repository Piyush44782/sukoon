"""Lightweight lexicon-based NLP: sentiment, emotions, concern topics.
Imperfect indicators only; not clinical assessments."""
import re

POS = set("happy good great calm relaxed better hopeful grateful excited proud fine okay confident peaceful "
          "motivated relieved enjoy enjoyed loved supported love cheerful improving".split())
NEG = set("sad stressed stress anxious anxiety worried worry lonely alone tired exhausted angry upset hopeless "
          "overwhelmed pressure scared afraid depressed cry crying hate failing failed panic nervous guilty "
          "worthless burnout burnt miserable confused lost struggling stuck tough hard difficult bad awful terrible "
          "disappointed drained rough down heavy unhappy".split())
NEGATORS = {"not", "no", "never", "don't", "dont", "can't", "cant", "isn't", "wasn't"}
EMOTIONS = {"Anxious": "anxious anxiety worried worry nervous panic scared afraid".split(),
            "Sad": "sad cry crying depressed miserable hopeless".split(),
            "Lonely": "lonely alone isolated".split(),
            "Overwhelmed": "overwhelmed pressure burnout burnt exhausted stressed stress".split(),
            "Angry": "angry hate upset frustrated".split(),
            "Hopeful/Positive": "happy hopeful grateful excited proud calm relaxed better".split()}
TOPICS = {"academic": "exam exams study studies marks grades assignment semester syllabus backlog attendance "
                      "concentrate concentration result results fail failing".split(),
          "career": "career job placement internship future resume interview course".split(),
          "family": "parents parent mom dad mother father family expect expectations home".split(),
          "relationship": "friend friends friendship relationship girlfriend boyfriend breakup partner "
                          "crush fight argument".split(),
          "isolation": "lonely alone isolated left-out nobody ignored outsider".split(),
          "distress": "hopeless worthless overwhelmed panic depressed exhausted burnout cry crying "
                      "anxious anxiety".split()}
TOPIC_LABELS = {"academic": "Academic pressure", "career": "Career concerns", "family": "Family concerns",
                "relationship": "Relationship difficulties", "isolation": "Social isolation",
                "distress": "General emotional distress"}

def analyze(text: str) -> dict:
    words = re.findall(r"[a-z']+", text.lower())
    score = 0
    for i, w in enumerate(words):
        s = 1 if w in POS else -1 if w in NEG else 0
        if s and i > 0 and words[i - 1] in NEGATORS:
            s = -s
        score += s
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    ws = set(words)
    return {"sentiment": sentiment, "score": score,
            "emotions": [e for e, k in EMOTIONS.items() if ws & set(k)],
            "topics": [t for t, k in TOPICS.items() if ws & set(k)]}
