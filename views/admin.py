"""Administrator interface. No access to chats, journals or individual wellness data."""
import streamlit as st
from core import data, auth

def render(u):
    auth.require_role(u, "admin")
    st.header("Administrator Dashboard")
    st.caption("Privacy by design: you can manage accounts and see anonymised aggregates, never private content.")
    t = st.tabs(["Approvals", "Students", "Resources", "Appointments", "Statistics", "Settings"])
    with t[0]:
        pp = data.pending_providers()
        for p in pp:
            with st.container(border=True):
                st.write(f"**{p['full_name']}** ({p['email']}) · {p['provider_type']} · {p['designation']}")
                c1, c2 = st.columns(2)
                if c1.button("Approve", key=f"ap{p['id']}"): data.approve_provider(p["id"]); st.rerun()
                if c2.button("Reject", key=f"rj{p['id']}"): data.reject_provider(p["id"]); st.rerun()
        if not pp: st.caption("No pending approvals. Verify real credentials before approving.")
    with t[1]:
        for s in data.students_list():
            c1, c2 = st.columns([4, 1])
            c1.write(f"{s['full_name']} · {s['email']} · {s['course']} Y{s['academic_year']}" + (" · DEMO" if s["is_demo"] else ""))
            if c2.button("Deactivate" if s["is_active"] else "Activate", key=f"st{s['id']}"):
                data.set_active(s["id"], not s["is_active"]); st.rerun()
    with t[2]:
        for r in data.list_resources():
            c1, c2 = st.columns([5, 1]); c1.write(f"**{r['category']}** · {r['title']}")
            if c2.button("Delete", key=f"dr{r['id']}"): data.delete_resource(r["id"]); st.rerun()
        with st.form("nr", clear_on_submit=True):
            c = st.text_input("Category"); ti = st.text_input("Title"); b = st.text_area("Content"); tg = st.text_input("Tags (comma-separated: academic,career,family,relationship,isolation,distress)")
            if st.form_submit_button("Add resource") and c and ti and b: data.add_resource(c, ti, b, tg); st.rerun()
    with t[3]:
        st.write("Appointment totals by status (no student details):")
        st.dataframe({"Status": [r["status"] for r in data.appointment_counts()], "Count": [r["n"] for r in data.appointment_counts()]})
    with t[4]:
        s = data.aggregate_stats()
        c1, c2, c3 = st.columns(3); c1.metric("Students", s["students"]); c2.metric("Check-ins (7d)", s["checkins_7d"])
        c3.metric("Avg mood (30d)", s["avg_mood"] if s["avg_mood"] else "Hidden (small group)")
        if s["topics"]: st.bar_chart(s["topics"])
        else: st.caption("Topic trends are hidden until enough students contribute (anonymity threshold).")
    with t[5]:
        op = st.checkbox("Student registration open", data.get_setting("registration_open", "1") == "1")
        if st.button("Save settings"): data.set_setting("registration_open", "1" if op else "0"); st.success("Saved.")
