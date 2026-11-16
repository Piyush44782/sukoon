"""SUKOON visual theme: deep indigo 'twilight' with violet, mint and soft coral accents.
The palette is locked in .streamlit/config.toml, so the browser's light/dark setting has no effect."""
import base64, functools
from pathlib import Path
import streamlit as st

LOGO = Path(__file__).parent / "assets" / "vips_logo.png"

@functools.lru_cache(maxsize=1)
def _logo_b64() -> str:
    return base64.b64encode(LOGO.read_bytes()).decode() if LOGO.exists() else ""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap');
html, body, [class*="css"], .stApp {font-family:'Nunito',sans-serif;}
.stApp {background:radial-gradient(1200px 600px at 85% -10%, #2A2468 0%, rgba(42,36,104,0) 60%), #12152B;}
[data-testid="stDecoration"], #MainMenu, footer, [data-testid="stHeaderActionElements"], .stDeployButton {display:none !important;}
[data-testid="stHeader"] {background:transparent; z-index:999; pointer-events:none;}
[data-testid="stToolbar"] {background:transparent; pointer-events:auto !important;}
[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"] {
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    pointer-events:auto !important;
    background:#1B1F3F !important;
    border:1px solid #3B4280 !important;
    border-radius:10px !important;
    color:#DAD6FF !important;
    box-shadow:0 4px 14px rgba(0,0,0,.45) !important;
    padding:6px 10px !important;
    margin-top:6px !important;
    margin-left:8px !important;
    transition:all .15s ease-in-out !important;
    cursor:pointer !important;
}
[data-testid="stExpandSidebarButton"]:hover, [data-testid="collapsedControl"]:hover {
    background:#2A2468 !important;
    border-color:#8B7CF6 !important;
    color:#FFFFFF !important;
    transform:scale(1.06);
}
[data-testid="stExpandSidebarButton"] *, [data-testid="collapsedControl"] * {
    color:#DAD6FF !important;
    fill:#DAD6FF !important;
}
[data-testid="stSidebarCollapseButton"] {
    color:#B4B9E0 !important;
    border-radius:8px !important;
    transition:all .15s !important;
}
[data-testid="stSidebarCollapseButton"]:hover {
    background:#1C2148 !important;
    color:#FFFFFF !important;
}
.block-container {padding-top:1.6rem; max-width:1100px;}
h1,h2,h3 {color:#DAD6FF !important; font-weight:700 !important; letter-spacing:-0.01em;}
p, label, span, li, div {color:#E6E8F5;}
small, .stCaption, [data-testid="stCaptionContainer"] * {color:#B4B9E0 !important;}

/* sidebar */
[data-testid="stSidebar"] {background:#0D1024; border-right:1px solid #232850;}
[data-testid="stSidebar"] [role="radiogroup"] {gap:4px;}
[data-testid="stSidebar"] [role="radiogroup"] label {padding:9px 14px; border-radius:12px; width:100%; cursor:pointer; transition:background .15s;}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {background:#1C2148;}
[data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div:first-child:not([data-testid="stMarkdownContainer"]) {display:none !important;}
[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"], [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:linear-gradient(90deg,#8B7CF6,#6C63E8);}
[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] *, [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * {color:#fff !important; font-weight:700;}
.brand {font-size:1.7rem !important; font-weight:700 !important; color:#C9C3FF !important; margin-bottom:0;}
.tag {font-size:.8rem !important; color:#A3A9D6 !important; margin-bottom:.8rem; line-height:1.3;}
.chip {display:inline-block; background:#2B2865; color:#D3CEFF !important; border-radius:20px; padding:2px 12px; font-size:.78rem; font-weight:600;}

/* cards, metrics, buttons */
[data-testid="stVerticalBlockBorderWrapper"] {background:#1B1F3F; border:1px solid #2B3166 !important; border-radius:18px !important; box-shadow:0 6px 20px rgba(0,0,0,.25);}
[data-testid="stMetric"] {background:#232857; border:1px solid #2F3570; border-radius:16px; padding:14px 18px;}
[data-testid="stMetricLabel"] p {color:#B9B2FF !important; font-weight:600;}
[data-testid="stMetricValue"] {color:#FFFFFF !important;}
.stButton>button, .stFormSubmitButton>button, .stDownloadButton>button {border-radius:12px; background:linear-gradient(90deg,#8B7CF6,#6C63E8); color:#fff !important; border:0; padding:.5rem 1.2rem; font-weight:600; transition:transform .1s, filter .15s;}
.stButton>button:hover, .stFormSubmitButton>button:hover {filter:brightness(1.12); transform:translateY(-1px);}
.stButton>button p, .stFormSubmitButton>button p {color:#fff !important;}
div[data-testid="stForm"] {background:#1B1F3F; border:1px solid #2B3166; border-radius:18px; padding:1.4rem;}
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"]>div {border-radius:12px !important; background:#141838 !important; border-color:#2E3468 !important;}
input, textarea {color:#E6E8F5 !important;}
input::placeholder, textarea::placeholder {color:#7F85B5 !important;}
[data-testid="stChatMessage"] {background:#1B1F3F; border:1px solid #2B3166; border-radius:18px; padding:.8rem 1rem;}
[data-testid="stChatInput"] {border-radius:16px;}
[data-testid="stExpander"] {background:#1B1F3F; border:1px solid #2B3166; border-radius:14px;}
[data-baseweb="tab-list"] {gap:6px;}
[data-baseweb="tab"] {border-radius:12px 12px 0 0;}
div[data-testid="stAlert"] {border-radius:14px;}

/* hero + logo badge */
.hero {display:flex; align-items:center; justify-content:space-between; gap:1.5rem; background:linear-gradient(120deg,#3A2F94 0%,#1F6F86 100%); border-radius:22px; padding:1.6rem 2rem; margin-bottom:1.2rem; border:1px solid rgba(255,255,255,.12);}
.hero h1 {margin:0 0 .3rem 0; font-size:2rem; color:#fff !important;}
.hero p {margin:0; color:#DCE6FF; font-size:1rem;}
.logo-badge {background:#F8F6F1; border-radius:14px; padding:8px 12px; box-shadow:0 4px 14px rgba(0,0,0,.28);}
.logo-badge img {display:block; width:100%; height:auto;}
.hero .logo-badge {width:170px; flex:none;}
.sb-logo {margin-top:1.2rem; padding-top:.9rem; border-top:1px solid #232850; font-size:.72rem; color:#8E94C4; letter-spacing:.04em; text-transform:uppercase;}
.sb-logo .logo-badge {margin-top:.4rem; width:150px;}
</style>
"""

def inject():
    st.markdown(CSS, unsafe_allow_html=True)

def _badge() -> str:
    b = _logo_b64()
    return f'<div class="logo-badge"><img alt="VIPS logo" src="data:image/png;base64,{b}"></div>' if b else ""

def hero(title: str, subtitle: str, logo: bool = False):
    right = _badge() if logo else ""
    st.markdown(f'<div class="hero"><div><h1>{title}</h1><p>{subtitle}</p></div>{right}</div>',
                unsafe_allow_html=True)

def sidebar_logo():
    st.sidebar.markdown(f'<div class="sb-logo">Made for students of{_badge()}</div>', unsafe_allow_html=True)
