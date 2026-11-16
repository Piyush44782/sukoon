"""Student interface: all ten sections."""
import streamlit as st
from datetime import date, datetime, timedelta
import config
from core import data, nlp, ai, safety, analytics, scheduler, auth

def _hist(msgs, new):
    h = [{"role": "user" if m["sender"] == "student" else "assistant", "content": m["text"]} for m in msgs]
    return h + [{"role": "user", "content": new}]

def home(u):
    sid = u["id"]
    import theme
    theme.hero(f"Welcome back, {u['full_name'].split()[0]} 🌿", "This is your space. Take a breath. Check in with yourself whenever you're ready.")
    if scheduler.checkin_due(sid):
        st.info("A gentle reminder: a quick check-in is available whenever you're ready. Open **Mood Check-in** (no pressure).")
    c1, c2, c3 = st.columns(3)
    rows = data.list_checkins(sid, 28)
    c1.metric("Check-ins (28 days)", len(rows)); c2.metric("Journal entries", len(data.list_journal(sid)))
    c3.metric("Conversations", len(data.list_conversations(sid)))
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.subheader("Quick mood check-in")
            m = st.slider("How are you feeling right now? (1 low - 5 great)", 1, 5, 3, key="qm")
            if st.button("Save mood"): data.add_checkin(sid, m); st.success("Saved."); st.rerun()
        with st.container(border=True):
            st.subheader("Weekly summary")
            for o in analytics.observations(rows)[:3]: st.write("• " + o)
    with right:
        with st.container(border=True):
            st.subheader("Mood trend")
            if rows: st.line_chart({"Mood": [r["mood"] for r in rows if r["mood"]]}, color=["#5EEAD4"], height=200)
            else: st.caption("Your mood history will appear here.")
        with st.container(border=True):
            st.subheader("Appointments")
            ap = [a for a in data.appointments_for(sid, "student") if a["status"] in ("pending", "accepted")]
            for a in ap[:3]: st.write(f"**{a['other_name']}**: {(a['slot_start'] or '')[:16].replace('T', ' ')} · _{a['status']}_")
            if not ap: st.caption("No upcoming appointments.")
    st.subheader("Helpful resources")
    cols = st.columns(3)
    for col, r in zip(cols, data.list_resources()[:3]):
        with col, st.container(border=True): st.markdown(f"**{r['title']}**"); st.caption(r["body"][:120] + "…")

def companion(u):
    sid = u["id"]
    st.header("AI Companion 💬")
    if not ai.api_ready():
        st.warning(f"AI service not configured for provider '{config.AI_PROVIDER}'. Replies will be basic.")
    if st.session_state.get("ai_err"): st.warning("AI service problem, using a basic reply: " + st.session_state.ai_err)
    st.caption("I'm an AI, not a counsellor or doctor, and I can't diagnose. " + safety.CONFIDENTIALITY_NOTE)
    with st.expander("AI status"):
        st.write(f"Provider: **{config.AI_PROVIDER}** · API key found: **{'yes' if ai.api_ready() else 'no'}**")
        if st.button("Test AI connection"):
            r = ai.reply([{"role": "user", "content": "Say hello in five words."}])
            if r == ai.FALLBACK: st.error("Connection failed: " + (ai.LAST_ERROR or "unknown error"))
            else: st.success("Working. Reply: " + r)
    convs = data.list_conversations(sid)
    if st.session_state.get("cid") not in [c["id"] for c in convs]:
        st.session_state.cid = convs[0]["id"] if convs else data.new_conversation(sid)
        convs = data.list_conversations(sid)
    ids = [c["id"] for c in convs]
    a, b, c = st.columns([4, 1, 1])
    st.session_state.cid = a.selectbox("Conversation", ids, index=ids.index(st.session_state.cid),
        format_func=lambda i: next(f"{x['title']} · {x['created_at'][:16]}" for x in convs if x["id"] == i))
    if b.button("➕ New"): st.session_state.cid = data.new_conversation(sid); st.rerun()
    if c.button("🗑 Delete"):
        data.delete_conversation(st.session_state.cid, sid); st.session_state.pop("cid"); st.rerun()
    cid = st.session_state.cid
    msgs = data.get_messages(cid, sid)
    for m in msgs:
        with st.chat_message("user" if m["sender"] == "student" else "assistant"): st.write(m["text"])
    last = st.session_state.get("last")
    if last and last["cid"] == cid:
        an = last["an"]
        if last["crisis"]: st.error("If you may be in danger, call **112** or Tele-MANAS **14416** now.")
        bits = [f"Tone: {an['sentiment']}"] + [nlp.TOPIC_LABELS[t] for t in an["topics"]] + an["emotions"]
        st.caption("Insights (imperfect, not a diagnosis): " + " · ".join(bits))
        recs = data.resources_for_topics(an["topics"] + (["crisis"] if last["crisis"] else []))
        if recs:
            with st.expander("Suggested resources"):
                for r in recs: st.markdown(f"**{r['title']}**\n\n{r['body']}")
        st.caption("Would you like to talk to a person? Open **Talk to Someone** in the menu.")
    if p := st.chat_input("Share what's on your mind…"):
        an = nlp.analyze(p); crisis = safety.detect_crisis(p)
        data.add_message(cid, sid, "student", p, an["sentiment"], an["topics"])
        if not msgs: data.rename_conversation(cid, sid, p)
        with st.spinner("Listening…"):
            rep = safety.CRISIS_REPLY if crisis else ai.reply(_hist(msgs, p), an)
        st.session_state.ai_err = ai.LAST_ERROR if rep == ai.FALLBACK else ""
        data.add_message(cid, sid, "ai", rep)
        st.session_state.last = {"cid": cid, "an": an, "crisis": crisis}; st.rerun()

def checkin(u):
    sid = u["id"]
    st.header("Mood Check-in 🌤")
    with st.form("ci"):
        mood = st.slider("How have you been feeling recently? (1 low - 5 great)", 1, 5, 3)
        stress = st.slider("How stressed have you been? (1 low - 5 high)", 1, 5, 3)
        sleep = st.slider("How has your sleep been? (1 poor - 5 great)", 1, 5, 3)
        over = st.slider("Academically overwhelmed? (1 not at all - 5 very)", 1, 5, 3)
        conn = st.slider("Socially connected? (1 not at all - 5 very)", 1, 5, 3)
        note = st.text_area("Is there anything you would like to discuss?")
        if st.form_submit_button("Submit check-in"):
            data.add_checkin(sid, mood, stress, sleep, over, conn, note); st.success("Thanks for checking in 💚"); st.rerun()
    rows = data.list_checkins(sid, 90)
    st.subheader("Previous check-ins")
    for r in reversed(rows[-10:]):
        st.write(f"**{r['created_at'][:16]}**: mood {r['mood']}, stress {r['stress']}, sleep {r['sleep']}, "
                 f"overwhelmed {r['overwhelmed']}, connected {r['connected']}" + (f"  \n_{r['note']}_" if r["note"] else ""))
    st.subheader("Reminder preferences")
    p = data.get_prefs(sid)
    with st.form("rp"):
        en = st.checkbox("Send me check-in reminders (about twice a week)", bool(p["reminders_enabled"]))
        pause = st.selectbox("Pause reminders", ["No pause", "1 week", "2 weeks", "1 month"])
        if st.form_submit_button("Save"):
            d = {"No pause": 0, "1 week": 7, "2 weeks": 14, "1 month": 30}[pause]
            data.set_prefs(sid, en, (datetime.now() + timedelta(days=d)).isoformat() if d else None, p["days"]); st.success("Saved.")
    st.caption("Missed check-ins are never treated as a sign that something is wrong.")

def analytics_page(u):
    sid = u["id"]
    st.header("Wellness Analytics 📈")
    st.caption("Based only on what you report. These are reflections, not diagnoses or labels.")
    rows = data.list_checkins(sid, 90)
    for o in analytics.observations(rows): st.info(o)
    if len(rows) >= 2:
        st.line_chart({k.title(): [r[k] for r in rows if r[k] is not None] for k in ("mood", "stress", "sleep")}, color=["#5EEAD4", "#FF9F80", "#A78BFA"])
        st.subheader("Weekly averages")
        st.dataframe({"Week": list(analytics.weekly_means(rows, "stress")),
                      "Mood": list(analytics.weekly_means(rows, "mood").values()),
                      "Stress": list(analytics.weekly_means(rows, "stress").values())}) if \
            len(analytics.weekly_means(rows, "mood")) == len(analytics.weekly_means(rows, "stress")) else None
    cs = data.chat_stats(sid)
    if cs:
        st.subheader("From your chats (imperfect signals)")
        sc, tc = {}, {}
        for m in cs:
            sc[m["sentiment"]] = sc.get(m["sentiment"], 0) + 1
            for t in filter(None, (m["topics"] or "").split(",")): tc[nlp.TOPIC_LABELS[t]] = tc.get(nlp.TOPIC_LABELS[t], 0) + 1
        c1, c2 = st.columns(2); c1.bar_chart(sc, color="#A78BFA"); c2.bar_chart(tc, color="#5EEAD4") if tc else c2.caption("No recurring themes yet.")

def journal(u):
    sid = u["id"]
    st.header("Private Journal 📓"); st.caption("Only you can see this. Entries are encrypted.")
    with st.expander("✍️ New entry", expanded=False):
        with st.form("nj", clear_on_submit=True):
            t = st.text_input("Title"); d = st.date_input("Date", date.today())
            cat = st.selectbox("Category", ["General", "Academics", "Family", "Friends", "Career", "Gratitude"])
            b = st.text_area("Write freely…", height=150)
            if st.form_submit_button("Save entry") and b.strip(): data.add_journal(sid, d, cat, t, b); st.rerun()
    s = st.text_input("🔍 Search journal")
    for e in data.list_journal(sid, s):
        with st.expander(f"{e['entry_date']} · {e['title'] or 'Untitled'} · {e['category']}"):
            with st.form(f"e{e['id']}"):
                t = st.text_input("Title", e["title"] or ""); b = st.text_area("Entry", e["body"], height=120)
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Update"): data.update_journal(e["id"], sid, e["entry_date"], e["category"], t, b); st.rerun()
                if c2.form_submit_button("Delete"): data.delete_journal(e["id"], sid); st.rerun()

def talk(u):
    sid = u["id"]
    st.header("Talk to Someone 🤝")
    st.caption(safety.CONFIDENTIALITY_NOTE)
    st.warning("Accounts marked DEMO are sample profiles for demonstration, not real VIPS staff. Peer mentors are trained students, not professionals.")
    tabs = st.tabs(list(config.PROVIDER_TYPES))
    for tab, ptype in zip(tabs, config.PROVIDER_TYPES):
        with tab:
            for p in data.list_providers(ptype):
                with st.container(border=True):
                    st.markdown(f"**{p['full_name']}**{' · DEMO' if p['is_demo'] else ''}  \n{p['designation']} · _{ptype}_")
                    st.write(f"**Expertise:** {p['expertise']}"); st.caption(p["intro"])
                    slots = data.open_slots(p["user_id"])
                    if not slots: st.caption("No available slots right now."); continue
                    sl = st.selectbox("Available time", [s["id"] for s in slots], key=f"s{p['user_id']}",
                                      format_func=lambda i, sl_=slots: next(s["slot_start"][:16].replace("T", " ") for s in sl_ if s["id"] == i))
                    note = st.text_input("Optional note for them", key=f"n{p['user_id']}")
                    if st.button("Request appointment", key=f"r{p['user_id']}"):
                        try: data.request_appointment(sid, p["user_id"], sl, note); st.success("Requested."); st.rerun()
                        except ValueError as e: st.error(str(e))
            if not data.list_providers(ptype): st.caption("No approved providers yet.")
    st.subheader("My appointments")
    for a in data.appointments_for(sid, "student"):
        with st.expander(f"{a['other_name']} · {(a['slot_start'] or '')[:16].replace('T', ' ')} · {a['status']}"):
            if a["status"] in ("pending", "accepted"):
                c1, c2 = st.columns(2)
                if c1.button("Cancel", key=f"c{a['id']}"): data.set_status(a["id"], sid, "student", "cancelled"); st.rerun()
                if c2.button("Reschedule (cancel, then pick a new time above)", key=f"rs{a['id']}"):
                    data.set_status(a["id"], sid, "student", "cancelled"); st.rerun()
            if a["status"] in ("pending", "accepted", "completed"): _msgs(a["id"], sid)

def _msgs(aid, uid):
    for m in data.appt_messages(aid, uid): st.write(f"**{m['full_name']}:** {m['text']}")
    with st.form(f"m{aid}", clear_on_submit=True):
        t = st.text_input("Message (protected channel)")
        if st.form_submit_button("Send") and t.strip(): data.post_appt_message(aid, uid, t); st.rerun()

def resources(u):
    st.header("Wellness Resources 🌿")
    rs = data.list_resources(); cats = sorted({r["category"] for r in rs})
    for tab, c in zip(st.tabs(cats), cats):
        with tab:
            for r in [x for x in rs if x["category"] == c]:
                with st.container(border=True): st.markdown(f"**{r['title']}**\n\n{r['body']}")

def parent(u):
    sid = u["id"]
    st.header("Parent Inclusion 👪")
    st.caption("You are in control. Parents never get automatic access to your profile, journal or chats.")
    c = data.current_consent(sid)
    labels = {"involve": "I want to involve my parents.", "selected": "I want to share selected information only.",
              "none": "I do not want to involve my parents right now."}
    st.write("**Current choice:** " + (labels[c["level"]] + f" _(since {c['granted_at'][:16]})_" if c else "None set yet"))
    with st.form("cs"):
        lv = st.radio("Your choice", list(labels), format_func=labels.get, index=list(labels).index(c["level"]) if c else 2)
        pn = st.text_input("Parent/guardian name", c["parent_name"] if c else "")
        pc = st.text_input("Parent/guardian contact", c["parent_contact"] if c else "")
        agree = st.checkbox("I understand I can review every item before it is shared and revoke consent anytime.")
        if st.form_submit_button("Save choice"):
            if lv != "none" and not (agree and pn.strip()): st.error("Please add a name and confirm your understanding.")
            else: data.set_consent(sid, lv, pn, pc); st.rerun()
    if c and c["level"] != "none":
        if st.button("Revoke consent"): data.revoke_consent(sid); st.rerun()
        st.subheader("Prepare something to share")
        kind = st.selectbox("What would you like to share?", data.KINDS[c["level"]])
        draft = ""
        if kind == "General wellness update":
            r = data.list_checkins(sid, 14)
            draft = "General update: " + ("; ".join(analytics.observations(r)[:2]) if r else "I'm doing okay and wanted to keep you in the loop.")
        elif kind == "Journal entry":
            es = data.list_journal(sid)
            if es:
                e = st.selectbox("Choose entry", es, format_func=lambda x: f"{x['entry_date']} · {x['title'] or 'Untitled'}")
                draft = f"{e['title']}\n\n{e['body']}"
            else: st.caption("No journal entries yet.")
        text = st.text_area("Review and edit exactly what will be shared", draft, height=140, key=f"sh{kind}{hash(draft)}")
        ok = st.checkbox("I have reviewed this and consent to share it.")
        if st.button("Share") and ok and text.strip():
            data.share_info(sid, kind, text); st.success("Recorded. Use the download below to send it to your parent.")
            st.download_button("Download shared message", text, "sukoon_shared.txt")
    st.subheader("Sharing history")
    for h in data.shared_history(sid):
        with st.expander(f"{h['shared_at'][:16]} · {h['kind']}" + (" · (consent since revoked)" if h["revoked_at"] else "")): st.write(h["text"])

def profile(u):
    sid = u["id"]; p = data.get_profile(sid)
    st.header("My Profile 👤")
    with st.form("pf"):
        n = st.text_input("Full name", p["full_name"]); st.text_input("Email", p["email"], disabled=True)
        c = st.selectbox("Course", config.COURSES, config.COURSES.index(p["course"]) if p["course"] in config.COURSES else 0)
        y = st.number_input("Year", 1, 5, p["academic_year"]); s = st.number_input("Semester", 1, 10, p["semester"])
        if st.form_submit_button("Update profile"): data.update_profile(sid, n, c, y, s); st.success("Updated.")
    with st.form("pw"):
        o = st.text_input("Current password", type="password"); nw = st.text_input("New password", type="password")
        if st.form_submit_button("Change password"):
            try: auth.change_password(sid, o, nw); st.success("Password changed.")
            except auth.AuthError as e: st.error(str(e))

def privacy(u):
    sid = u["id"]
    st.header("Privacy Settings 🔒")
    st.markdown("- Only you can see your chats, journal and check-ins. Admins see **aggregate, anonymised** numbers only.\n"
                "- Sensitive text is encrypted at rest.\n- " + safety.CONFIDENTIALITY_NOTE)
    st.subheader("Delete my data")
    for k, lab in (("conversations", "all AI conversations"), ("journal", "all journal entries"), ("checkins", "all check-ins")):
        if st.button(f"Delete {lab}"): st.session_state.confirm = k
    if (k := st.session_state.get("confirm")):
        st.error(f"This permanently deletes {k}.")
        if st.button("Yes, delete permanently"): data.delete_my_data(sid, k); st.session_state.pop("confirm"); st.success("Deleted."); st.rerun()
    st.divider()
    if st.checkbox("I want to delete my entire account") and st.button("Delete account permanently"):
        data.delete_account(sid); st.session_state.clear(); st.rerun()

PAGES = {"Home": home, "AI Companion": companion, "Mood Check-in": checkin, "Wellness Analytics": analytics_page,
         "Private Journal": journal, "Talk to Someone": talk, "Wellness Resources": resources,
         "Parent Inclusion": parent, "My Profile": profile, "Privacy Settings": privacy}

def render(u):
    auth.require_role(u, "student")
    PAGES[st.sidebar.radio("Menu", list(PAGES))](u)
    st.sidebar.markdown("---"); st.sidebar.caption("Need help now? Call 112 or Tele-MANAS 14416")
