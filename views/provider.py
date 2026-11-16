"""Counsellor / mentor interface. Providers see only their own appointments."""
import streamlit as st
from datetime import datetime, time
from core import data, auth
from views.student import _msgs
import config

def render(u):
    auth.require_role(u, "counsellor", "mentor"); pid = u["id"]
    st.header("Support Provider Dashboard")
    t1, t2, t3, t4 = st.tabs(["Requests", "Sessions", "Availability", "My profile"])
    aps = data.appointments_for(pid, "provider")
    with t1:
        for a in [x for x in aps if x["status"] == "pending"]:
            with st.container(border=True):
                st.write(f"**{a['other_name']}** · {(a['slot_start'] or '')[:16].replace('T', ' ')}")
                if a["note"]: st.caption("Student note: " + a["note"])
                c1, c2 = st.columns(2)
                if c1.button("Accept", key=f"a{a['id']}"): data.set_status(a["id"], pid, u["role"], "accepted"); st.rerun()
                if c2.button("Reject", key=f"x{a['id']}"): data.set_status(a["id"], pid, u["role"], "rejected"); st.rerun()
        if not any(x["status"] == "pending" for x in aps): st.caption("No pending requests.")
    with t2:
        for a in [x for x in aps if x["status"] in ("accepted", "completed")]:
            with st.expander(f"{a['other_name']} · {(a['slot_start'] or '')[:16].replace('T', ' ')} · {a['status']}"):
                if a["status"] == "accepted" and st.button("Mark completed", key=f"d{a['id']}"):
                    data.set_status(a["id"], pid, u["role"], "completed"); st.rerun()
                _msgs(a["id"], pid)
    with t3:
        with st.form("slot"):
            d = st.date_input("Date"); h = st.time_input("Time", time(11, 0))
            if st.form_submit_button("Add slot"): data.add_slot(pid, datetime.combine(d, h)); st.rerun()
        for s in data.open_slots(pid): st.write("• " + s["slot_start"][:16].replace("T", " "))
    with t4:
        p = data.q("SELECT * FROM provider_profiles WHERE user_id=?", (pid,), one=True)
        st.write(f"**Type:** {p['provider_type']}  (shown to students exactly as registered)")
        with st.form("pp"):
            de = st.text_input("Designation", p["designation"] or ""); ex = st.text_input("Area of expertise", p["expertise"] or "")
            it = st.text_area("Short introduction", p["intro"] or "")
            if st.form_submit_button("Save"): data.update_provider_profile(pid, de, ex, it); st.success("Saved.")
