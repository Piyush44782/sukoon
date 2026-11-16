"""SUKOON entry point: login / registration and role-based routing (Phase 1)."""
import streamlit as st
import config
from core.database import init_db
from core import auth, data
from core.resources_seed import seed_resources
import os

st.set_page_config(page_title=config.APP_NAME, page_icon="🌿", layout="wide", initial_sidebar_state="expanded")
init_db(); seed_resources()
from seed import seed as seed_demo_accounts; seed_demo_accounts()
try:
    for _k in ("GROQ_API_KEY", "ANTHROPIC_API_KEY", "SUKOON_GROQ_MODEL", "SUKOON_MODEL"):
        if _k in st.secrets:
            os.environ[_k] = st.secrets[_k]
            if _k == "SUKOON_GROQ_MODEL":
                import config as _c; _c.GROQ_MODEL = st.secrets[_k]
    if "SUKOON_AI_PROVIDER" in st.secrets:
        os.environ["SUKOON_AI_PROVIDER"] = st.secrets["SUKOON_AI_PROVIDER"]
        import config as _c; _c.AI_PROVIDER = st.secrets["SUKOON_AI_PROVIDER"].lower()
except Exception:
    pass

import theme
theme.inject()

def auth_screen():
    theme.hero(f"🌿 {config.APP_NAME}", config.TAGLINE + "<br><span class='chip'>Exclusively for VIPS Pitampura students</span>", logo=True)
    tab_in, tab_reg, tab_pr = st.tabs(["Log in", "Student registration", "Counsellor / Mentor sign-up"])
    with tab_in:
        with st.form("login"):
            email = st.text_input("Email"); pw = st.text_input("Password", type="password")
            if st.form_submit_button("Log in"):
                try:
                    st.session_state.user = auth.login(email, pw); st.rerun()
                except auth.AuthError as e:
                    st.error(str(e))
        st.caption("Demo accounts (synthetic, not real VIPS staff): student.demo@vips.edu / Demo@1234")
    with tab_reg:
        with st.form("register"):
            name = st.text_input("Full name"); email = st.text_input("VIPS email")
            c1, c2, c3 = st.columns(3)
            course = c1.selectbox("Course", config.COURSES)
            year = c2.number_input("Year", 1, 5, 1); sem = c3.number_input("Semester", 1, 10, 1)
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Create account"):
                if data.get_setting("registration_open", "1") != "1":
                    st.error("Registration is currently closed."); st.stop()
                try:
                    auth.register_student(name, email, pw, course, year, sem)
                    st.success("Account created. Please log in.")
                except auth.AuthError as e:
                    st.error(str(e))

    with tab_pr:
        with st.form("prov"):
            n = st.text_input("Full name"); e = st.text_input("VIPS email"); pt = st.selectbox("I am a", config.PROVIDER_TYPES)
            de = st.text_input("Designation"); ex = st.text_input("Area of expertise"); it = st.text_area("Short introduction")
            pw = st.text_input("Password", type="password", key="ppw")
            if st.form_submit_button("Request account"):
                try:
                    auth.register_provider(n, e, pw, pt, de, ex, it); st.success("Submitted. An administrator must approve your account before you can log in.")
                except auth.AuthError as err:
                    st.error(str(err))

def home(user):
    with st.sidebar:
        st.markdown(f"<p class='brand'>🌿 {config.APP_NAME}</p><p class='tag'>{config.TAGLINE}</p>", unsafe_allow_html=True)
        st.markdown(f"**{user['full_name']}**  \n<span class='chip'>{user['role'].title()}{' · DEMO' if user['is_demo'] else ''}</span>", unsafe_allow_html=True)
        if st.button("Log out"):
            st.session_state.pop("user"); st.rerun()
    from views import student, provider, admin
    {"student": student.render, "counsellor": provider.render, "mentor": provider.render, "admin": admin.render}[user["role"]](user)
    theme.sidebar_logo()

user = st.session_state.get("user")
if user:
    home(user)
else:
    auth_screen()
