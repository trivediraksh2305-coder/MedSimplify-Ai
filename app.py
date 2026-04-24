import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
# Import all utils
from utils.pdf_reader import extract_text
from utils.ai_simplifier import simplify_report
from utils.highlighter import highlight_abnormal
from utils.translator import translate_text, LANGUAGES
from utils.tooltips import get_tooltips
from utils.voice import text_to_speech
from utils.advice import get_personalized_advice
from utils.auth import init_db, login_user, register_user
from database.db import save_report, get_user_reports
load_dotenv()
init_db()
st.set_page_config(
    page_title="MedSimplify AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* FORCE EVERYTHING BLACK */
html, body, div, p, span, label, h1, h2, h3, h4, h5, h6,
input, textarea, select, option, li, a, small, strong, em {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
input, textarea { background: #ffffff !important; }

/* FORCE SIDEBAR ALWAYS VISIBLE */
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    transform: none !important;
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}
[data-testid="stSidebar"] button[kind="header"],
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* Sidebar background */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0a2e1a 0%, #0f3d22 60%, #145c30 100%) !important;
}

/* Sidebar white text for everything EXCEPT the selectbox */
[data-testid="stSidebar"] { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ══ SIDEBAR SELECTBOX — WHITE BOX, BLACK TEXT ══ */
/* Outer container */
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: transparent !important;
}
/* The visible box */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #ffffff !important;
    background-color: #ffffff !important;
    border: 2px solid #22a355 !important;
    border-radius: 8px !important;
}
/* Value container and single value (SELECTED TEXT) */
[data-testid="stSidebar"] [data-baseweb="select"] [class*="ValueContainer"],
[data-testid="stSidebar"] [data-baseweb="select"] [class*="singleValue"],
[data-testid="stSidebar"] [data-baseweb="select"] [class*="placeholder"],
[data-testid="stSidebar"] [data-baseweb="select"] [class*="Input"],
[data-testid="stSidebar"] [data-baseweb="select"] input {
    background: transparent !important;
    background-color: transparent !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
/* Every span/div/p inside selectbox → BLACK */
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="select"] p {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background: transparent !important;
    background-color: transparent !important;
}
/* Arrow icon green */
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #22a355 !important;
    color: #22a355 !important;
}

/* ══ DROPDOWN POPUP — white bg, black text ══ */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
ul[data-baseweb="menu"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    border: 1px solid #22a355 !important;
    border-radius: 8px !important;
}
[data-baseweb="option"],
li[data-baseweb="option"],
[role="option"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
[data-baseweb="option"] *,
li[data-baseweb="option"] *,
[role="option"] * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
[data-baseweb="option"]:hover,
li[data-baseweb="option"]:hover {
    background: #e8faf0 !important;
    background-color: #e8faf0 !important;
}
[aria-selected="true"][role="option"],
[aria-selected="true"][data-baseweb="option"] {
    background: #d4f5e3 !important;
    background-color: #d4f5e3 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* ══ ALL BUTTONS BASE ══ */
.stButton > button {
    background: linear-gradient(135deg, #22a355, #1a7a3f) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    white-space: nowrap !important;
    width: 100% !important;
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    line-height: 1.2 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2ecc6e, #22a355) !important;
    transform: translateY(-1px) !important;
}
.stButton > button p, .stButton > button span, .stButton > button div {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    white-space: nowrap !important;
    font-size: 14px !important;
    line-height: 1.2 !important;
}

/* Sidebar logout button */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 14px !important;
    min-height: 36px !important;
    max-height: 36px !important;
    height: 36px !important;
    width: 100% !important;
    white-space: nowrap !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.2) !important;
    transform: none !important;
}
[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] .stButton > button span,
[data-testid="stSidebar"] .stButton > button div {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 13px !important;
    white-space: nowrap !important;
}

/* Browse files button */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploader"] button {
    background: #ffffff !important;
    border: 2px solid #22a355 !important;
    border-radius: 8px !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 600 !important;
    min-height: 36px !important;
    max-height: 36px !important;
    height: 36px !important;
    padding: 6px 16px !important;
    white-space: nowrap !important;
    width: auto !important;
}
[data-testid="stFileUploaderDropzone"] button span,
[data-testid="stFileUploader"] button span,
[data-testid="stFileUploaderDropzone"] button p,
[data-testid="stFileUploader"] button p {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Scroll */
html { scroll-behavior: auto !important; }
html, body { overflow-anchor: none !important; }
section.main, .main, [data-testid="stAppViewContainer"] { scroll-behavior: auto !important; }
[data-testid="stAppViewContainer"] > section.main { overflow-y: auto !important; overflow-anchor: none !important; }
#top-anchor { position: absolute; top: 0; left: 0; height: 0; width: 0; }

/* App background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0f7f2 0%, #e8f5ec 50%, #f5faf6 100%) !important;
}

/* Hide streamlit chrome */
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.stDeployButton { display: none; }
header { visibility: visible !important; background: transparent !important; }
header * { visibility: visible !important; }

[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: #22a355 !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    box-shadow: 0 2px 10px rgba(34,163,85,0.5) !important;
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 9999 !important;
    cursor: pointer !important;
}
[data-testid="collapsedControl"] * {
    visibility: visible !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    fill: white !important;
    stroke: white !important;
}
[data-testid="collapsedControl"] svg { width: 20px !important; height: 20px !important; }

/* Inputs */
.stTextInput label, .stTextInput label * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 600 !important;
}
.stTextInput input {
    border: 2px solid #c8d5ca !important;
    border-radius: 8px !important;
    background: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
.stTextInput input:focus {
    border-color: #22a355 !important;
    box-shadow: 0 0 0 3px rgba(34,163,85,0.12) !important;
}
.stTextInput [data-testid="InputInstructions"],
[data-testid="InputInstructions"],
div[data-testid="InputInstructions"] { display: none !important; visibility: hidden !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #e8ede9 !important; border-radius: 8px !important; padding: 4px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border-radius: 6px !important; }
.stTabs [data-baseweb="tab"] * { color: #5a6b5c !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: white !important; box-shadow: 0 2px 8px rgba(10,46,26,0.08) !important; }
.stTabs [aria-selected="true"] * { color: #1a7a3f !important; font-weight: 600 !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #5ddb91 !important;
    border-radius: 14px !important;
    background: rgba(34,163,85,0.03) !important;
    padding: 12px !important;
}
[data-testid="stFileUploader"] * { color: #000000 !important; -webkit-text-fill-color: #000000 !important; }

/* Dropzone */
[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(135deg, #1a7a3f, #22a355) !important;
    border-radius: 10px !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzone"] * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background: #ffffff !important;
}

/* Expander */
[data-testid="stExpander"] { border: 1px solid #e8ede9 !important; border-radius: 8px !important; background: white !important; }

/* Alerts */
.stSuccess { background: linear-gradient(135deg,#e8faf0,#d4f5e3) !important; border-left: 4px solid #22a355 !important; border-radius: 8px !important; }
.stError   { border-left: 4px solid #e05252 !important; border-radius: 8px !important; }
.stInfo    { border-left: 4px solid #3a9bd5 !important; border-radius: 8px !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f7f9f7; }
::-webkit-scrollbar-thumb { background: #5ddb91; border-radius: 3px; }

/* Chat messages */
.chat-message-user {
    background: linear-gradient(135deg, #22a355, #1a7a3f);
    color: white !important;
    -webkit-text-fill-color: white !important;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 20%;
    font-size: 14px;
    line-height: 1.6;
}
.chat-message-bot {
    background: #f0f7f2;
    border: 1px solid #a8f0c6;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 20% 8px 0;
    font-size: 14px;
    line-height: 1.6;
}
.chat-message-user * { color: white !important; -webkit-text-fill-color: white !important; }
.chat-message-bot  * { color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

# ─── JS FIX ───────────────────────────────────────
st.markdown("""
<script>
function scrollToTop() {
    try {
        var main = window.parent.document.querySelector('.main');
        if(main) main.scrollTop = 0;
        var main2 = window.parent.document.querySelector('section.main');
        if(main2) main2.scrollTop = 0;
        var block = window.parent.document.querySelector('.block-container');
        if(block) block.scrollTop = 0;
        window.parent.document.documentElement.scrollTop = 0;
        window.parent.document.body.scrollTop = 0;
        window.parent.scrollTo(0,0);
        window.scrollTo(0,0);
    } catch(e){}
}
scrollToTop();
[100,300,600].forEach(t => setTimeout(scrollToTop, t));

function fixColors() {
    // ── Browse files button ──
    document.querySelectorAll('[data-testid="stFileUploaderDropzone"] button, [data-testid="stFileUploader"] button').forEach(el => {
        el.style.setProperty('background-color', '#ffffff', 'important');
        el.style.setProperty('border', '2px solid #22a355', 'important');
        el.style.setProperty('color', '#000000', 'important');
        el.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
        el.querySelectorAll('*').forEach(c => {
            c.style.setProperty('color', '#000000', 'important');
            c.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
        });
    });

    // ── Input labels & fields ──
    document.querySelectorAll('.stTextInput label, .stTextInput label *').forEach(el => {
        el.style.setProperty('color', '#000000', 'important');
        el.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
    });
    document.querySelectorAll('.stTextInput input').forEach(el => {
        el.style.setProperty('color', '#000000', 'important');
        el.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
        el.style.setProperty('background', '#ffffff', 'important');
    });

    // ── SIDEBAR SELECTBOX: white bg, BLACK text ──
    // Step 1: outer box white
    document.querySelectorAll('[data-testid="stSidebar"] [data-baseweb="select"] > div').forEach(el => {
        el.style.setProperty('background',       '#ffffff', 'important');
        el.style.setProperty('background-color', '#ffffff', 'important');
        el.style.setProperty('border',           '2px solid #22a355', 'important');
        el.style.setProperty('border-radius',    '8px', 'important');
    });

    // Step 2: EVERY child inside selectbox → black text, transparent bg
    document.querySelectorAll('[data-testid="stSidebar"] [data-baseweb="select"] *').forEach(el => {
        var tag = (el.tagName || '').toLowerCase();
        // skip the SVG arrow — make it green
        if (tag === 'svg' || tag === 'path' || tag === 'polyline' || tag === 'line') {
            el.style.setProperty('fill',   '#22a355', 'important');
            el.style.setProperty('stroke', '#22a355', 'important');
            el.style.setProperty('color',  '#22a355', 'important');
            return;
        }
        el.style.setProperty('color',                '#000000', 'important');
        el.style.setProperty('-webkit-text-fill-color','#000000','important');
        el.style.setProperty('background',           'transparent', 'important');
        el.style.setProperty('background-color',     'transparent', 'important');
    });

    // Step 3: dropdown popup options
    document.querySelectorAll('[data-baseweb="option"], [role="option"]').forEach(el => {
        el.style.setProperty('background',       '#ffffff', 'important');
        el.style.setProperty('background-color', '#ffffff', 'important');
        el.style.setProperty('color',            '#000000', 'important');
        el.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
        el.querySelectorAll('*').forEach(c => {
            c.style.setProperty('color', '#000000', 'important');
            c.style.setProperty('-webkit-text-fill-color', '#000000', 'important');
        });
    });
    document.querySelectorAll('[data-baseweb="menu"], [data-baseweb="popover"] > div').forEach(el => {
        el.style.setProperty('background',       '#ffffff', 'important');
        el.style.setProperty('background-color', '#ffffff', 'important');
    });
}

fixColors();
[300, 800, 2000, 4000].forEach(t => setTimeout(fixColors, t));
new MutationObserver(fixColors).observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────
if 'logged_in'    not in st.session_state: st.session_state.logged_in    = False
if 'username'     not in st.session_state: st.session_state.username     = ""
if 'user_id'      not in st.session_state: st.session_state.user_id      = None
if 'report_text'  not in st.session_state: st.session_state.report_text  = ""
if 'simplified'   not in st.session_state: st.session_state.simplified   = ""
if 'chat_history' not in st.session_state: st.session_state.chat_history = []


# ══════════════════════════════════════════════════
#  AI CHATBOT FUNCTION
# ══════════════════════════════════════════════════
def chat_with_ai(user_message, report_text, chat_history):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        messages = [{
            "role": "system",
            "content": f"""You are a helpful medical assistant chatbot called MedBot.
You help patients understand their medical reports in simple, friendly language.
You answer questions about medical terms, test results, and health advice.
Always be empathetic, clear, and avoid technical jargon.
If you don't know something, say so honestly.
Never diagnose — always recommend consulting a doctor for serious concerns.

Here is the patient's medical report for context:
{report_text if report_text else 'No report uploaded yet. Answer general medical questions.'}

Keep answers concise and friendly. Use bullet points when listing multiple items."""
        }]
        for msg in chat_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I couldn't process your question right now. Error: {str(e)}"


# ══════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════
def show_login():
    st.markdown("""
    <div style="text-align:center;padding:60px 20px 50px;
        background:linear-gradient(135deg,#0a2e1a 0%,#145c30 50%,#0f3d22 100%);
        border-radius:24px;margin-bottom:36px;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;bottom:0;
            background:radial-gradient(circle at 20% 50%,rgba(46,204,110,0.15) 0%,transparent 60%),
                       radial-gradient(circle at 80% 50%,rgba(34,163,85,0.1) 0%,transparent 60%);">
        </div>
        <div style="position:relative;z-index:1;">
            <div style="display:inline-flex;align-items:center;justify-content:center;
                width:80px;height:80px;background:linear-gradient(135deg,#22a355,#2ecc6e);
                border-radius:20px;font-size:38px;margin-bottom:20px;
                box-shadow:0 8px 32px rgba(34,163,85,0.4);">🌿</div>
            <h1 style="font-family:'Playfair Display',serif;font-size:52px;font-weight:700;
                color:white;margin:0 0 12px;letter-spacing:-1px;">
                MedSimplify <span style="color:#5ddb91;">AI</span></h1>
            <p style="font-size:18px;color:rgba(255,255,255,0.65);margin:0 0 36px;font-weight:300;">
                Your Medical Report, Explained in Simple Words</p>
            <div style="display:flex;justify-content:center;gap:40px;flex-wrap:wrap;">
                <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:#5ddb91;">AI</div><div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:rgba(255,255,255,0.5);">Powered</div></div>
                <div style="width:1px;background:rgba(255,255,255,0.15);"></div>
                <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:#5ddb91;">10+</div><div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:rgba(255,255,255,0.5);">Languages</div></div>
                <div style="width:1px;background:rgba(255,255,255,0.15);"></div>
                <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:#5ddb91;">Free</div><div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:rgba(255,255,255,0.5);">To Use</div></div>
                <div style="width:1px;background:rgba(255,255,255,0.15);"></div>
                <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:#5ddb91;">🤖</div><div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:rgba(255,255,255,0.5);">AI Chat</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:36px;">
        <div style="background:white;border-radius:16px;padding:24px 16px;text-align:center;box-shadow:0 2px 16px rgba(10,46,26,0.07);border-top:3px solid #22a355;">
            <div style="font-size:32px;margin-bottom:12px;">📄</div><h3 style="font-family:'Playfair Display',serif;font-size:15px;color:#0a2e1a;margin:0 0 6px;">Upload PDF</h3><p style="font-size:12px;color:#5a6b5c;margin:0;line-height:1.5;">Upload any medical report PDF</p></div>
        <div style="background:white;border-radius:16px;padding:24px 16px;text-align:center;box-shadow:0 2px 16px rgba(10,46,26,0.07);border-top:3px solid #22a355;">
            <div style="font-size:32px;margin-bottom:12px;">🤖</div><h3 style="font-family:'Playfair Display',serif;font-size:15px;color:#0a2e1a;margin:0 0 6px;">AI Simplifies</h3><p style="font-size:12px;color:#5a6b5c;margin:0;line-height:1.5;">Complex terms in plain language</p></div>
        <div style="background:white;border-radius:16px;padding:24px 16px;text-align:center;box-shadow:0 2px 16px rgba(10,46,26,0.07);border-top:3px solid #22a355;">
            <div style="font-size:32px;margin-bottom:12px;">💬</div><h3 style="font-family:'Playfair Display',serif;font-size:15px;color:#0a2e1a;margin:0 0 6px;">AI Chatbot</h3><p style="font-size:12px;color:#5a6b5c;margin:0;line-height:1.5;">Ask questions about your report</p></div>
        <div style="background:white;border-radius:16px;padding:24px 16px;text-align:center;box-shadow:0 2px 16px rgba(10,46,26,0.07);border-top:3px solid #22a355;">
            <div style="font-size:32px;margin-bottom:12px;">🌍</div><h3 style="font-family:'Playfair Display',serif;font-size:15px;color:#0a2e1a;margin:0 0 6px;">Multilingual</h3><p style="font-size:12px;color:#5a6b5c;margin:0;line-height:1.5;">Hindi, Gujarati & 8 more</p></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("""
        <div style="background:white;border-radius:20px;padding:32px;
            box-shadow:0 8px 40px rgba(10,46,26,0.12);
            border:1px solid rgba(34,163,85,0.12);margin-bottom:8px;">
            <div style="text-align:center;margin-bottom:20px;">
                <h2 style="font-family:'Playfair Display',serif;font-size:26px;color:#0a2e1a;margin:0 0 6px;">Welcome Back</h2>
                <p style="color:#5a6b5c;font-size:14px;margin:0;">Sign in to access your health dashboard</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐   Login", "📝   Register"])

        with tab1:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username", key="login_user")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Sign In  →", key="login_btn"):
                if not username or not password:
                    st.error("⚠️ Please enter both username and password")
                else:
                    result = login_user(username, password)
                    if result:
                        st.session_state.logged_in    = True
                        st.session_state.username     = username
                        st.session_state.user_id      = result
                        st.session_state.chat_history = []
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Wrong username or password")

        with tab2:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            new_user  = st.text_input("Username",         placeholder="Choose a username",    key="reg_user")
            new_email = st.text_input("Email",            placeholder="your@email.com",        key="reg_email")
            new_pass  = st.text_input("Password",         type="password",
                                      placeholder="Create a strong password",                  key="reg_pass")
            conf_pass = st.text_input("Confirm Password", type="password",
                                      placeholder="Repeat your password",                      key="reg_conf")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Create Account  →", key="reg_btn"):
                if not new_user or not new_email or not new_pass:
                    st.error("⚠️ Please fill all fields")
                elif new_pass != conf_pass:
                    st.error("❌ Passwords do not match")
                else:
                    if register_user(new_user, new_pass, new_email):
                        st.success("✅ Account created! Please login.")
                    else:
                        st.error(f"❌ Username **'{new_user}'** already exists.")


# ══════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════
def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:24px 0 12px;text-align:center;">
            <div style="display:inline-flex;align-items:center;justify-content:center;
                width:60px;height:60px;background:linear-gradient(135deg,#22a355,#2ecc6e);
                border-radius:16px;font-size:30px;margin-bottom:12px;
                box-shadow:0 4px 16px rgba(34,163,85,0.4);">🌿</div>
            <h2 style="font-family:'Playfair Display',serif;font-size:20px;
                font-weight:700;color:white;margin:0;">MedSimplify AI</h2>
            <p style="font-size:12px;color:rgba(255,255,255,0.4);margin:4px 0 0;">
                Medical Report Simplifier</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin:8px 0 16px'>",
                    unsafe_allow_html=True)

        initial = st.session_state.username[0].upper() if st.session_state.username else "U"
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.08);border-radius:12px;
            padding:14px 16px;margin-bottom:20px;border:1px solid rgba(255,255,255,0.1);">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:38px;height:38px;flex-shrink:0;
                    background:linear-gradient(135deg,#22a355,#2ecc6e);border-radius:50%;
                    display:flex;align-items:center;justify-content:center;
                    font-size:16px;font-weight:700;color:white;">{initial}</div>
                <div>
                    <div style="font-weight:600;font-size:14px;color:white;">{st.session_state.username}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.4);">Active Session</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size:11px;font-weight:600;text-transform:uppercase;
            letter-spacing:1.5px;color:rgba(255,255,255,0.4);margin:0 0 8px;">
            🌍 Output Language
        </p>
        """, unsafe_allow_html=True)

        lang = st.selectbox("lang_select", list(LANGUAGES.keys()), label_visibility="collapsed")

        st.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin:16px 0'>",
                    unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size:11px;font-weight:600;text-transform:uppercase;
            letter-spacing:1.5px;color:rgba(255,255,255,0.4);margin:0 0 12px;">
            📋 Recent Reports
        </p>
        """, unsafe_allow_html=True)

        if st.session_state.user_id:
            reports = get_user_reports(st.session_state.user_id)
            if reports:
                for i, r in enumerate(reports[:4]):
                    name = (r[0] or f"Report {i+1}")[:20]
                    date = r[2][:10] if r[2] else ""
                    with st.expander(f"📄 {name}"):
                        st.write(f"🗓️ {date}")
                        if r[1]: st.write(r[1][:100] + "...")
            else:
                st.markdown("""
                <div style="background:rgba(255,255,255,0.06);border-radius:8px;
                    padding:14px;text-align:center;color:rgba(255,255,255,0.35);font-size:13px;">
                    No reports saved yet
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin:16px 0'>",
                    unsafe_allow_html=True)

        if st.button("🚪   Logout", key="logout_btn"):
            st.session_state.logged_in    = False
            st.session_state.username     = ""
            st.session_state.user_id      = None
            st.session_state.report_text  = ""
            st.session_state.simplified   = ""
            st.session_state.chat_history = []
            st.rerun()

    return lang


# ══════════════════════════════════════════════════
#  CHATBOT SECTION
# ══════════════════════════════════════════════════
def show_chatbot():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a7a3f,#22a355);
        border-radius:18px;padding:24px 28px 20px;margin-bottom:0px;">
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:48px;height:48px;background:rgba(255,255,255,0.2);
                border-radius:12px;display:flex;align-items:center;justify-content:center;
                font-size:24px;">🤖</div>
            <div>
                <h3 style="font-family:'Playfair Display',serif;font-size:20px;
                    color:white;-webkit-text-fill-color:white;margin:0 0 4px;">
                    MedBot - AI Assistant</h3>
                <p style="color:rgba(255,255,255,0.85);-webkit-text-fill-color:rgba(255,255,255,0.85);
                    font-size:13px;margin:0;">Ask me anything about your medical report</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Ask MedBot",
            placeholder="Type your question about the medical report...",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col_send:
        send_clicked = st.button("Send 📨", key="send_btn", use_container_width=True)

    if send_clicked and user_input.strip():
        handle_chat_message(user_input.strip())

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    with st.container():
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="chat-message-bot">
                👋 Hello! I'm <strong>MedBot</strong>, your AI medical assistant.<br><br>
                I can help you understand your medical report. Here are some things you can ask me:<br>
                • <em>"What does hemoglobin mean?"</em><br>
                • <em>"Is my WBC count normal?"</em><br>
                • <em>"What foods help increase platelets?"</em><br>
                • <em>"Should I be worried about my results?"</em><br><br>
                Upload your report above and feel free to ask me anything! 😊
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-message-user"><strong>You:</strong> {msg["content"]}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message-bot"><strong>🤖 MedBot:</strong> {msg["content"]}</div>',
                            unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <p style="color:#5a6b5c;font-size:13px;font-weight:600;margin:16px 0 10px;">
            💡 Quick Questions — click to ask:
        </p>
        """, unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        r2c1, r2c2 = st.columns(2)
        with r1c1:
            if st.button("🔬  What is CBC?", key="q1", use_container_width=True):
                handle_chat_message("What is CBC (Complete Blood Count)?")
        with r1c2:
            if st.button("📋  Explain my results", key="q2", use_container_width=True):
                handle_chat_message("Can you explain my test results in simple words?")
        with r2c1:
            if st.button("🥗  What should I eat?", key="q3", use_container_width=True):
                handle_chat_message("What foods should I eat to improve my health?")
        with r2c2:
            if st.button("🏥  Do I need a doctor?", key="q4", use_container_width=True):
                handle_chat_message("Should I see a doctor urgently based on my report?")

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()


def handle_chat_message(message):
    st.session_state.chat_history.append({"role": "user", "content": message})
    with st.spinner("🤖 MedBot is thinking..."):
        response = chat_with_ai(
            message,
            st.session_state.report_text,
            st.session_state.chat_history[:-1]
        )
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()


# ══════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════
def show_main_app():
    lang = show_sidebar()

    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    st.markdown("""
    <script>
    (function(){
        function goTop(){
            try {
                var main = window.parent.document.querySelector('.main');
                if(main) main.scrollTop = 0;
                var main2 = window.parent.document.querySelector('section.main');
                if(main2) main2.scrollTop = 0;
                var block = window.parent.document.querySelector('.block-container');
                if(block) block.scrollTop = 0;
                window.parent.document.documentElement.scrollTop = 0;
                window.parent.document.body.scrollTop = 0;
                window.parent.scrollTo(0,0);
            } catch(e){}
        }
        goTop();
        [100,300,600].forEach(t => setTimeout(goTop, t));
    })();
    </script>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a7a3f 0%,#22a355 60%,#2ecc6e 100%);
        border-radius:20px;padding:36px 40px;margin-bottom:32px;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-40px;right:-40px;width:220px;height:220px;
            background:radial-gradient(circle,rgba(255,255,255,0.15) 0%,transparent 70%);border-radius:50%;"></div>
        <div style="position:relative;z-index:1;">
            <p style="color:rgba(255,255,255,0.8);font-size:12px;text-transform:uppercase;
                letter-spacing:2px;margin:0 0 8px;-webkit-text-fill-color:rgba(255,255,255,0.8);">
                Health Dashboard</p>
            <h1 style="font-family:'Playfair Display',serif;font-size:34px;
                color:#ffffff;-webkit-text-fill-color:#ffffff;margin:0 0 10px;">
                Medical Report Simplifier</h1>
            <p style="color:rgba(255,255,255,0.85);-webkit-text-fill-color:rgba(255,255,255,0.85);
                font-size:15px;margin:0;">
                Upload your report · Get AI insights · Chat with MedBot</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    main_tab1, main_tab2 = st.tabs(["📄   Report Analysis", "💬   MedBot Chat"])

    # ════════════════════════════
    #  TAB 1 — REPORT ANALYSIS
    # ════════════════════════════
    with main_tab1:
        st.markdown("""
        <div style="background:white;border-radius:18px;padding:28px 32px;margin-bottom:20px;
            box-shadow:0 2px 16px rgba(10,46,26,0.07);border:1px solid rgba(34,163,85,0.1);">
            <h3 style="font-family:'Playfair Display',serif;font-size:20px;color:#0a2e1a;margin:0 0 6px;">
                📤 Upload Medical Report</h3>
            <p style="color:#5a6b5c;font-size:14px;margin:0;">
                Supported: CBC, Blood Test, Urine Test and more · PDF format only</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drop your PDF here or click to browse",
            type=["pdf"],
            help="Upload any medical report in PDF format"
        )

        if not uploaded_file:
            st.markdown("""
            <div style="background:white;border-radius:18px;padding:60px 40px;text-align:center;
                box-shadow:0 2px 16px rgba(10,46,26,0.07);margin-top:20px;">
                <div style="font-size:64px;margin-bottom:20px;">🏥</div>
                <h3 style="font-family:'Playfair Display',serif;font-size:26px;color:#0a2e1a;margin:0 0 12px;">
                    Ready to Simplify Your Report</h3>
                <p style="color:#5a6b5c;font-size:15px;max-width:420px;margin:0 auto 32px;line-height:1.7;">
                    Upload a medical PDF above to receive an AI-powered explanation in simple language.</p>
                <div style="display:inline-flex;gap:28px;background:#f0f7f2;border-radius:12px;padding:16px 32px;">
                    <span style="color:#22a355;font-size:14px;font-weight:500;">✅ CBC Reports</span>
                    <span style="color:#22a355;font-size:14px;font-weight:500;">✅ Blood Tests</span>
                    <span style="color:#22a355;font-size:14px;font-weight:500;">✅ Urine Tests</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("📖 Reading your medical report..."):
                report_text = extract_text(uploaded_file)

            if not report_text or len(report_text.strip()) < 20:
                st.error("❌ Could not read the PDF. Please upload a clear, readable PDF.")
                return

            st.session_state.report_text = report_text

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#e8faf0,#d4f5e3);border:1px solid #a8f0c6;
                border-left:4px solid #22a355;border-radius:12px;padding:16px 20px;margin:16px 0 28px;
                display:flex;align-items:center;gap:14px;">
                <span style="font-size:26px;">✅</span>
                <div>
                    <div style="font-weight:700;color:#0a2e1a;font-size:15px;">Report Read Successfully</div>
                    <div style="color:#1a7a3f;font-size:13px;margin-top:2px;">
                        {len(report_text)} characters extracted · Ready for AI analysis ·
                        <strong>Switch to MedBot tab to ask questions!</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📄 View Raw Extracted Text"):
                st.markdown(f"""
                <div style="background:#f7f9f7;border-radius:8px;padding:16px;font-family:monospace;
                    font-size:13px;color:#2d3a2e;white-space:pre-wrap;line-height:1.6;
                    max-height:300px;overflow-y:auto;border:1px solid #e8ede9;">
                    {report_text}
                </div>
                """, unsafe_allow_html=True)

            abnormal_df = highlight_abnormal(report_text)
            tooltips    = get_tooltips(report_text)

            c1, c2, c3 = st.columns(3)
            with c1:
                color = "#e05252" if not abnormal_df.empty else "#22a355"
                icon  = "⚠️"      if not abnormal_df.empty else "✅"
                st.markdown(f"""
                <div style="background:white;border-radius:14px;padding:22px;text-align:center;
                    box-shadow:0 2px 12px rgba(10,46,26,0.07);border-top:3px solid {color};margin-bottom:20px;">
                    <div style="font-size:28px;margin-bottom:6px;">{icon}</div>
                    <div style="font-size:30px;font-weight:700;color:{color};">{len(abnormal_df)}</div>
                    <div style="font-size:13px;color:#5a6b5c;font-weight:500;margin-top:4px;">Abnormal Values</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="background:white;border-radius:14px;padding:22px;text-align:center;
                    box-shadow:0 2px 12px rgba(10,46,26,0.07);border-top:3px solid #3a9bd5;margin-bottom:20px;">
                    <div style="font-size:28px;margin-bottom:6px;">💡</div>
                    <div style="font-size:30px;font-weight:700;color:#3a9bd5;">{len(tooltips)}</div>
                    <div style="font-size:13px;color:#5a6b5c;font-weight:500;margin-top:4px;">Terms Explained</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div style="background:white;border-radius:14px;padding:22px;text-align:center;
                    box-shadow:0 2px 12px rgba(10,46,26,0.07);border-top:3px solid #c9a84c;margin-bottom:20px;">
                    <div style="font-size:28px;margin-bottom:6px;">📊</div>
                    <div style="font-size:30px;font-weight:700;color:#c9a84c;">{len(report_text.split())}</div>
                    <div style="font-size:13px;color:#5a6b5c;font-weight:500;margin-top:4px;">Words Analyzed</div>
                </div>
                """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div style="background:white;border-radius:16px;padding:24px;
                    box-shadow:0 2px 12px rgba(10,46,26,0.07);margin-bottom:24px;">
                    <h3 style="font-family:'Playfair Display',serif;font-size:18px;
                        color:#0a2e1a;margin:0 0 16px;">⚠️ Abnormal Values</h3>
                </div>
                """, unsafe_allow_html=True)
                if not abnormal_df.empty:
                    st.dataframe(abnormal_df, use_container_width=True, hide_index=True)
                else:
                    st.success("✅ All detected values are within normal range!")

            with col2:
                st.markdown("""
                <div style="background:white;border-radius:16px;padding:24px;
                    box-shadow:0 2px 12px rgba(10,46,26,0.07);margin-bottom:24px;">
                    <h3 style="font-family:'Playfair Display',serif;font-size:18px;
                        color:#0a2e1a;margin:0 0 16px;">💡 Medical Terms Explained</h3>
                </div>
                """, unsafe_allow_html=True)
                if tooltips:
                    for term, meaning in tooltips.items():
                        st.markdown(f"""
                        <div style="background:#f0f7f2;border-left:3px solid #22a355;
                            border-radius:8px;padding:10px 14px;margin-bottom:8px;">
                            <span style="font-weight:600;color:#0a2e1a;font-size:14px;">{term}</span>
                            <br><span style="color:#5a6b5c;font-size:13px;">{meaning}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ No specific medical terms detected")

            st.markdown("""
            <div style="background:white;border-radius:18px;padding:28px 32px 20px;
                box-shadow:0 2px 16px rgba(10,46,26,0.07);margin-bottom:8px;
                border:1px solid rgba(34,163,85,0.1);">
                <h3 style="font-family:'Playfair Display',serif;font-size:22px;
                    color:#0a2e1a;margin:0 0 6px;">🤖 AI Simplified Report</h3>
                <p style="color:#5a6b5c;font-size:14px;margin:0;">
                    Your report explained in simple, easy-to-understand language</p>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("🤖 AI is analyzing your report..."):
                simplified = simplify_report(report_text)

            st.session_state.simplified = simplified

            if lang != "English":
                with st.spinner(f"🌍 Translating to {lang}..."):
                    simplified = translate_text(simplified, LANGUAGES[lang])

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a7a3f,#22a355);border-radius:16px;padding:32px;
                font-family:'DM Sans',sans-serif;font-size:15px;line-height:1.9;
                color:white;-webkit-text-fill-color:white;
                box-shadow:0 4px 24px rgba(34,163,85,0.25);margin-bottom:28px;">
                {simplified.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            col3, col4 = st.columns(2)
            with col3:
                st.markdown("""
                <div style="background:white;border-radius:16px;padding:24px;
                    box-shadow:0 2px 12px rgba(10,46,26,0.07);margin-bottom:16px;">
                    <h3 style="font-family:'Playfair Display',serif;font-size:18px;
                        color:#0a2e1a;margin:0 0 6px;">🔊 Voice Playback</h3>
                    <p style="color:#5a6b5c;font-size:13px;margin:0 0 16px;">Listen to your simplified report</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("▶️   Generate Audio", key="audio_btn"):
                    with st.spinner("🎵 Generating audio..."):
                        audio_file = text_to_speech(simplified, LANGUAGES[lang])
                        if audio_file:
                            st.audio(audio_file)
                            st.success("✅ Audio ready!")
                        else:
                            st.error("❌ Could not generate audio")

            with col4:
                st.markdown("""
                <div style="background:white;border-radius:16px;padding:24px;
                    box-shadow:0 2px 12px rgba(10,46,26,0.07);margin-bottom:16px;">
                    <h3 style="font-family:'Playfair Display',serif;font-size:18px;
                        color:#0a2e1a;margin:0 0 6px;">💾 Save Report</h3>
                    <p style="color:#5a6b5c;font-size:13px;margin:0 0 16px;">Save this report to your history</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("💾   Save to History", key="save_btn"):
                    if st.session_state.user_id:
                        save_report(st.session_state.user_id,
                                    uploaded_file.name, report_text, simplified)
                        st.success("✅ Report saved!")

            st.markdown("""
            <div style="background:linear-gradient(135deg,#f0f7f2,#e8faf0);border-radius:18px;
                padding:28px 32px 20px;box-shadow:0 2px 16px rgba(10,46,26,0.07);
                border:1px solid #a8f0c6;margin-bottom:12px;">
                <h3 style="font-family:'Playfair Display',serif;font-size:22px;
                    color:#0a2e1a;margin:0 0 6px;">💊 Personalized Health Advice</h3>
                <p style="color:#5a6b5c;font-size:14px;margin:0;">
                    AI-generated advice based on your specific report findings</p>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("💭 Generating personalized advice..."):
                advice = get_personalized_advice(abnormal_df, report_text)

            if lang != "English":
                advice = translate_text(advice, LANGUAGES[lang])

            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:28px;border-left:4px solid #22a355;
                box-shadow:0 2px 12px rgba(10,46,26,0.07);font-family:'DM Sans',sans-serif;
                font-size:15px;line-height:1.8;color:#2d3a2e;margin-bottom:40px;">
                {advice.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

    # ════════════════════════════
    #  TAB 2 — MEDBOT CHAT
    # ════════════════════════════
    with main_tab2:
        show_chatbot()


# ══════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════
if st.session_state.logged_in:
    show_main_app()
else:
    show_login()