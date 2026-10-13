# ============================================================
# Vexa AI — Gemini 3 chatbot
# Streamlit + Google Gemini 3
# ============================================================

import os, sys, html, time
import streamlit as st

SDK_IMPORT_ERROR = None
try:
    from google import genai
    from google.genai import types
except Exception as e:
    genai = None
    types = None
    SDK_IMPORT_ERROR = f"{type(e).__name__}: {e}"

# ------------------------------------------------------------------
# Favicon
# ------------------------------------------------------------------
VEXA_FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E"
    "%3Cstop offset='0' stop-color='%238b6cff'/%3E"
    "%3Cstop offset='1' stop-color='%236743ee'/%3E"
    "%3C/linearGradient%3E%3C/defs%3E"
    "%3Crect width='32' height='32' rx='9' fill='url(%23g)'/%3E"
    "%3Cpath d='M16 7l2.1 6.4L24.5 15l-6.4 2.1L16 23.5l-2.1-6.4L7.5 15l6.4-1.6z'"
    " fill='white'/%3E%3C/svg%3E"
)

st.set_page_config(
    page_title="Vexa AI",
    page_icon=VEXA_FAVICON,
    layout="centered",
    initial_sidebar_state="expanded",
)

FALLBACK_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
]

SYSTEM_PROMPT = (
    "You are Vexa AI, a helpful, intelligent, friendly AI assistant. "
    "Give accurate, clear, well-structured answers. Use Markdown and code "
    "blocks where helpful. If you are uncertain, say so clearly."
)

# ------------------------------------------------------------------
# CSS  (same as before — unchanged)
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root{
    --bg:#ffffff; --text:#0d0d0d; --muted:#8e8ea0; --line:#e5e5e5;
    --bubble:#f4f4f4; --sidebar:#171717; --sidebar-hover:#2f2f2f;
    --sidebar-text:#ececec; --sidebar-muted:#7a7a7a;
    --accent:#7557ff; --accent-soft:#a78bfa;
}
html, body, .stApp, [class*="css"], button, textarea, input{
    font-family:'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
                Roboto, sans-serif !important;
}
.stApp{ background: var(--bg) !important; color: var(--text) !important; }
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"]{ display:none !important; }
[data-testid="stHeader"]{ background: transparent !important; height: 2.4rem !important; }
.block-container{
    max-width: 780px !important;
    padding-left: 1.5rem !important; padding-right: 1.5rem !important;
    padding-top: 1.2rem !important; padding-bottom: 9rem !important;
}
[data-testid="stSidebar"]{
    background: var(--sidebar) !important;
    border-right: none !important;
    width: 278px !important; min-width: 278px !important;
}
[data-testid="stSidebar"] > div:first-child{
    background: var(--sidebar) !important;
    padding: 0.5rem 0.6rem 1rem 0.6rem !important;
}
[data-testid="stSidebar"] *{ color: var(--sidebar-text); }
[data-testid="stSidebar"] hr{ border-color:#2b2b2b !important; margin: 10px 4px !important; }

.vexa-brand-row{ display:flex; align-items:center; gap:10px; padding: 6px 10px 14px 10px; }
.vexa-mark{
    width:30px; height:30px; border-radius:9px;
    background: linear-gradient(135deg,#8b6cff,#6743ee);
    display:flex; align-items:center; justify-content:center;
    color:#fff !important; font-size:15px; font-weight:700;
    box-shadow: 0 4px 12px rgba(117,87,255,.28); flex-shrink: 0;
}
.vexa-name{ font-size:16px; font-weight:600; color:#ffffff !important; letter-spacing:-.2px; }
.vexa-name span{ color: var(--accent-soft) !important; }

.side-label{
    font-size:11px; font-weight:600; letter-spacing:.8px;
    text-transform:uppercase; color: var(--sidebar-muted) !important;
    padding: 14px 12px 6px 12px;
    display:flex; align-items:center; gap:6px;
}
.side-label::before{
    content:""; display:inline-block; width:3px; height:11px;
    background: linear-gradient(180deg,#8b6cff,#6743ee); border-radius:2px;
}
[data-testid="stSidebar"] .stButton > button{
    width:100% !important; background: transparent !important;
    border: none !important; border-radius: 10px !important;
    color: var(--sidebar-text) !important; font-size: 14px !important;
    font-weight: 450 !important; padding: 9px 12px !important;
    text-align: left !important; justify-content: flex-start !important;
    box-shadow: none !important; min-height: 38px !important;
    transition: background .15s ease, color .15s ease !important;
}
[data-testid="stSidebar"] .stButton > button p{
    font-size: 14px !important; font-weight: 450 !important;
    color: var(--sidebar-text) !important;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin: 0 !important;
}
[data-testid="stSidebar"] .stButton > button:hover{ background: var(--sidebar-hover) !important; }
[data-testid="stSidebar"] .stButton > button:hover p{ color:#ffffff !important; }
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:active{ box-shadow: none !important; outline: none !important; }

[data-testid="stSidebar"] [data-baseweb="select"] > div{
    background: #242424 !important; border: 1px solid #343434 !important;
    border-radius: 10px !important; color: #ececec !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] *{ color: #ececec !important; }
[data-testid="stSidebar"] [data-baseweb="select"] svg{ fill: #ececec !important; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{
    color:#6f6f6f !important; font-size: 12px !important; letter-spacing:.2px;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{ color: var(--sidebar-text); }

[data-testid="stSidebar"] .stDownloadButton > button{
    width:100% !important; background:#1f1f1f !important;
    border:1px solid #2e2e2e !important; border-radius:10px !important;
    color:#ececec !important; font-size:13.5px !important; font-weight:500 !important;
    padding:9px 12px !important; text-align:left !important;
    justify-content:flex-start !important; box-shadow:none !important;
}
[data-testid="stSidebar"] .stDownloadButton > button:hover{
    background:#262626 !important; border-color:#3a3a3a !important;
}
[data-testid="stSidebar"] .stDownloadButton > button p{ color:#ececec !important; }

[data-testid="stSidebar"] details{
    background:#1e1e1e !important; border:1px solid #2b2b2b !important;
    border-radius: 10px !important; padding: 4px 8px !important; margin-top: 4px !important;
}
[data-testid="stSidebar"] details summary{
    font-size:13px !important; font-weight:500 !important;
    color:#cfcfcf !important; padding: 6px 4px !important;
}
[data-testid="stSidebar"] details *{ color:#ececec !important; }
[data-testid="stSidebar"] details code{
    background:#0d0d0d !important; color:#d6d6d6 !important; font-size:11.5px !important;
}

.hero{
    text-align:center; font-size:29px; font-weight:600;
    letter-spacing:-.6px; color:#0d0d0d !important; margin: 14vh 0 10px 0;
}
.hero-sub{
    text-align:center; font-size:14px; color:#8e8ea0;
    margin-bottom: 34px; letter-spacing:-.1px;
}
.stButton > button{
    width: 100% !important; background:#ffffff !important;
    border:1px solid var(--line) !important; border-radius:14px !important;
    color:#0d0d0d !important; font-size:14px !important; font-weight:450 !important;
    padding: 13px 15px !important; text-align:left !important;
    justify-content:flex-start !important; box-shadow:none !important;
    min-height: 46px !important;
    transition: background .15s ease, border-color .15s ease, box-shadow .15s ease !important;
}
.stButton > button p{ font-size:14px !important; font-weight:450 !important; color:#0d0d0d !important; }
.stButton > button:hover{
    background:#f7f7f8 !important; border-color:#d4d4d8 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.04) !important;
}
.stButton > button:hover p{ color:#0d0d0d !important; }

.user-row{ display:flex; justify-content:flex-end; margin: 22px 0 6px 0; }
.user-bubble{
    background: var(--bubble); color:#0d0d0d !important;
    border-radius: 20px; padding: 10px 18px; max-width: 78%;
    font-size: 15.5px; line-height: 1.65; white-space: pre-wrap; overflow-wrap: anywhere;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] div,
[data-testid="stMarkdownContainer"] a{ color:#0d0d0d !important; }
[data-testid="stMarkdownContainer"] a{
    text-decoration: underline; text-underline-offset: 2px;
    text-decoration-color:#b0b0bd;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{ font-size: 15.5px; line-height: 1.75; }

[data-testid="stMarkdownContainer"] h1{
    font-size:24px !important; font-weight:700 !important;
    margin: 22px 0 10px 0 !important; line-height:1.3 !important; letter-spacing:-.3px !important;
}
[data-testid="stMarkdownContainer"] h2{
    font-size:20px !important; font-weight:650 !important;
    margin: 20px 0 8px 0 !important; line-height:1.3 !important; letter-spacing:-.2px !important;
}
[data-testid="stMarkdownContainer"] h3{
    font-size:17px !important; font-weight:600 !important;
    margin: 18px 0 6px 0 !important; line-height:1.35 !important;
}
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6{
    font-size:15.5px !important; font-weight:600 !important; margin: 16px 0 6px 0 !important;
}
[data-testid="stMarkdownContainer"] blockquote{
    border-left:3px solid #d4d4d8 !important; padding-left:14px !important; margin: 12px 0 !important;
}
[data-testid="stMarkdownContainer"] blockquote *{ color:#52525b !important; }
[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol{ padding-left: 22px !important; margin: 8px 0 !important; }

[data-testid="stMarkdownContainer"] code{
    background:#f0f0f2; color:#0d0d0d !important; padding:2px 6px; border-radius:6px;
    font-size:13.5px; font-family:'SF Mono', Menlo, Consolas, monospace;
}
[data-testid="stMarkdownContainer"] pre{
    background:#0d0d0d !important; border:1px solid #262626 !important;
    border-radius:12px !important; padding:14px 16px !important;
    overflow-x:auto; margin: 12px 0 !important;
}
[data-testid="stMarkdownContainer"] pre code,
[data-testid="stMarkdownContainer"] pre span{
    background: transparent !important; color:#f5f5f5 !important;
    font-size:13.5px !important; padding: 0 !important;
    font-family:'SF Mono', Menlo, Consolas, monospace !important;
}

[data-testid="stMarkdownContainer"] table{
    border-collapse: collapse !important; margin: 12px 0 !important; font-size: 14.5px !important;
}
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] td{
    border:1px solid #e5e5e5 !important; padding: 8px 12px !important; color:#0d0d0d !important;
}
[data-testid="stMarkdownContainer"] th{ background:#f7f7f8 !important; font-weight:600 !important; }

div[data-testid="stAlert"]{ border-radius: 12px !important; font-size: 14px; }

[data-testid="stBottom"]{ background: #ffffff !important; }
[data-testid="stBottom"] > div{ background: transparent !important; }
[data-testid="stBottomBlockContainer"]{
    max-width: 780px !important;
    padding-left: 1.5rem !important; padding-right: 1.5rem !important;
    padding-bottom: 1.2rem !important;
}
[data-testid="stChatInput"]{
    background:#ffffff !important; border:1px solid #d9d9e3 !important;
    border-radius: 26px !important; box-shadow: 0 2px 12px rgba(0,0,0,.06) !important;
    padding: 4px 8px 4px 10px !important; overflow: hidden;
}
[data-testid="stChatInput"] > div{ border: none !important; background: transparent !important; }
[data-testid="stChatInput"] textarea{
    background: transparent !important; color:#0d0d0d !important;
    font-size: 15.5px !important;
    padding-top: 10px !important; padding-bottom: 10px !important;
}
[data-testid="stChatInput"] textarea::placeholder{ color:#8e8ea0 !important; }
[data-testid="stChatInputSubmitButton"]{
    background:#0d0d0d !important; border-radius: 50% !important;
}
[data-testid="stChatInputSubmitButton"] svg{ fill:#ffffff !important; color:#ffffff !important; }
[data-testid="stChatInputSubmitButton"]:hover{ background:#333333 !important; }

.input-hint{
    text-align:center; color:#b0b0bd; font-size:11.5px;
    margin-top:-2px; letter-spacing:.1px;
}
.input-hint kbd{
    background:#f2f2f4; border:1px solid #e0e0e4; border-radius:4px;
    padding:1px 5px; font-size:10.5px;
    font-family:'SF Mono', Menlo, Consolas, monospace; color:#52525b;
}

@media (prefers-color-scheme: dark){
    [data-testid="stMarkdownContainer"] *{ color:#0d0d0d !important; }
    .stApp{ background:#ffffff !important; }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SDK guard
# ------------------------------------------------------------------
if SDK_IMPORT_ERROR:
    st.error("Could not import `google-genai`.")
    st.code(SDK_IMPORT_ERROR)
    st.stop()

# ------------------------------------------------------------------
# API key: Streamlit secrets -> env var
# ------------------------------------------------------------------
api_key = ""
try:
    api_key = (st.secrets.get("GEMINI_API_KEY", "") or "").strip()
except Exception:
    pass
if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

if not api_key:
    st.error(
        "GEMINI_API_KEY is not set. Add it to `.streamlit/secrets.toml` "
        "(local) or Streamlit Cloud → Settings → Secrets."
    )
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to create genai client: {e}")
    st.stop()

# ------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------
ss = st.session_state
if "chats" not in ss:
    ss.chats = {}
    ss.chat_counter = 0
    ss.active_chat = None
if "pending" not in ss:
    ss.pending = None
if "last_error" not in ss:
    ss.last_error = None
if "model_options" not in ss:
    try:
        fetched = []
        for m in client.models.list():
            name = (getattr(m, "name", "") or "").replace("models/", "")
            if not name.startswith("gemini-3"):
                continue
            if any(b in name for b in ("embedding", "aqa", "imagen", "veo", "tts")):
                continue
            fetched.append(name)
        ss.model_options = fetched or list(FALLBACK_MODELS)
    except Exception:
        ss.model_options = list(FALLBACK_MODELS)
    for f in FALLBACK_MODELS:
        if f not in ss.model_options:
            ss.model_options.append(f)

def new_chat():
    ss.chat_counter += 1
    cid = str(ss.chat_counter)
    ss.chats[cid] = {"title": "New chat", "messages": [], "ts": time.time()}
    ss.active_chat = cid
    return cid

def delete_chat(cid):
    ss.chats.pop(cid, None)
    if not ss.chats:
        new_chat()
    elif ss.active_chat == cid:
        ss.active_chat = next(iter(ss.chats))

if ss.active_chat is None or ss.active_chat not in ss.chats:
    new_chat()

def bubble(text):
    safe = html.escape(text).strip().replace("\n", "<br>")
    st.markdown(
        f'<div class="user-row"><div class="user-bubble">{safe}</div></div>',
        unsafe_allow_html=True,
    )

def make_part(text):
    try:
        return types.Part.from_text(text=text)
    except Exception:
        return types.Part(text=text)

def build_config(model):
    kwargs = dict(system_instruction=SYSTEM_PROMPT, max_output_tokens=8192)
    if model.startswith("gemini-3"):
        return types.GenerateContentConfig(**kwargs)
    return types.GenerateContentConfig(**kwargs, temperature=0.7)

def chat_to_markdown(chat):
    lines = [f"# {chat['title']}\n"]
    for m in chat["messages"]:
        role = "You" if m["role"] == "user" else "Vexa AI"
        lines.append(f"**{role}:**\n\n{m['content']}\n\n---\n")
    return "\n".join(lines)

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="vexa-brand-row">
        <div class="vexa-mark">✦</div>
        <div class="vexa-name">Vexa <span>AI</span></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋   New chat", use_container_width=True, key="new"):
        new_chat(); st.rerun()

    st.markdown('<div class="side-label">Model</div>', unsafe_allow_html=True)
    MODEL = st.selectbox(
        "model", ss.model_options, index=0,
        label_visibility="collapsed",
        help="Loaded from your API key. gemini-3.5-flash is a good default.",
    )

    st.markdown('<div class="side-label">Chats</div>', unsafe_allow_html=True)

    for cid, chat in reversed(list(ss.chats.items())):
        title = chat["title"]
        shown = title[:22] + ("…" if len(title) > 22 else "")
        is_active = (cid == ss.active_chat)
        marker = "◆" if is_active else "◇"
        c_open, c_del = st.columns([6, 1])
        with c_open:
            if st.button(f"{marker}  {shown}", key="open_" + cid, use_container_width=True):
                ss.active_chat = cid; st.rerun()
        with c_del:
            if st.button("✕", key="del_" + cid, use_container_width=True):
                delete_chat(cid); st.rerun()

    st.markdown("---")

    if ss.active_chat and ss.chats[ss.active_chat]["messages"]:
        md = chat_to_markdown(ss.chats[ss.active_chat])
        st.download_button(
            "↧   Export chat",
            data=md,
            file_name=f"vexa_chat_{ss.active_chat}.md",
            mime="text/markdown",
            use_container_width=True,
            key="dl_" + ss.active_chat,
        )

    if st.button("⌫   Clear all", use_container_width=True, key="clear"):
        ss.chats = {}; ss.active_chat = None; ss.last_error = None
        new_chat(); st.rerun()

    with st.expander("⚙  Diagnostics", expanded=False):
        st.write("Python:", sys.version.split()[0])
        st.write("Streamlit:", st.__version__)
        try:
            import google.genai as _g
            st.write("google-genai:", getattr(_g, "__version__", "unknown"))
        except Exception as e:
            st.write("version lookup failed:", e)
        st.write("Key prefix:", api_key[:6] + "...")
        st.write("Model:", MODEL)

    if st.button("▶   Test API", use_container_width=True, key="testapi"):
        with st.spinner("Calling Gemini…"):
            try:
                resp = client.models.generate_content(
                    model=MODEL,
                    contents=[types.Content(role="user",
                                            parts=[make_part("Say OK")])],
                )
                st.success("API call succeeded.")
                st.code((resp.text or "(empty)")[:500])
            except Exception as e:
                st.error("API call failed.")
                st.code(f"{type(e).__name__}: {e}")

    st.caption("Vexa AI  ·  Powered by Google Gemini 3")

# ------------------------------------------------------------------
# Active chat
# ------------------------------------------------------------------
chat = ss.chats[ss.active_chat]
messages = chat["messages"]

if ss.last_error:
    st.error(ss.last_error); ss.last_error = None

# ------------------------------------------------------------------
# Welcome
# ------------------------------------------------------------------
if not messages and not ss.pending:
    st.markdown('<div class="hero">What can I help with?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Ask anything — code, writing, ideas, explanations.</div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✦  Explain something", use_container_width=True):
            ss.pending = "Explain how artificial intelligence works with simple examples."; st.rerun()
        if st.button("◇  Help me code", use_container_width=True):
            ss.pending = "Teach me Python programming with examples and best practices."; st.rerun()
    with c2:
        if st.button("✎  Write something", use_container_width=True):
            ss.pending = "Help me write a clear, professional document."; st.rerun()
        if st.button("✦  Brainstorm ideas", use_container_width=True):
            ss.pending = "Suggest five useful AI project ideas with features and stacks."; st.rerun()

# ------------------------------------------------------------------
# History
# ------------------------------------------------------------------
for m in messages:
    if m["role"] == "user":
        bubble(m["content"])
    else:
        st.markdown(m["content"])

if messages and messages[-1]["role"] == "assistant":
    if st.button("↻  Regenerate", key="regen"):
        messages.pop()
        st.rerun()

# ------------------------------------------------------------------
# Input
# ------------------------------------------------------------------
user_prompt = st.chat_input("Message Vexa AI…", key="chat_input")

st.markdown(
    '<div class="input-hint"><kbd>Enter</kbd> to send · '
    '<kbd>Shift</kbd>+<kbd>Enter</kbd> for a new line</div>',
    unsafe_allow_html=True,
)

if not user_prompt and ss.pending:
    user_prompt = ss.pending
    ss.pending = None

# Single-phase submission — no intermediate rerun
if user_prompt and user_prompt.strip():
    user_prompt = user_prompt.strip()

    if not messages:
        chat["title"] = user_prompt[:30] + ("…" if len(user_prompt) > 30 else "")

    messages.append({"role": "user", "content": user_prompt})
    bubble(user_prompt)

    with st.spinner("Vexa is thinking…"):
        try:
            history = messages[-20:]
            if history and history[0]["role"] != "user":
                history = history[1:]

            contents = [
                types.Content(
                    role=("user" if m["role"] == "user" else "model"),
                    parts=[make_part(m["content"])],
                )
                for m in history
            ]

            resp = client.models.generate_content(
                model=MODEL, contents=contents, config=build_config(MODEL),
            )

            try:
                answer = resp.text
            except Exception:
                answer = None
            if not answer:
                answer = ("(empty response — try a shorter prompt or "
                          "another model)")

            messages.append({"role": "assistant", "content": answer})
            st.markdown(answer)

        except Exception as e:
            err = f"{type(e).__name__}: {e}"
            low = err.lower()
            if "404" in err or "not_found" in low or "not found" in low:
                ss.last_error = f"Model `{MODEL}` not available for this key."
            elif "api_key_invalid" in low or "permission_denied" in low or "401" in err or "403" in err:
                ss.last_error = "API key invalid or lacks access to this model."
            elif "resource_exhausted" in low or "429" in err or "quota" in low:
                ss.last_error = "Quota / rate limit exceeded. Wait and retry."
            else:
                ss.last_error = f"Request failed: {err[:400]}"
            if messages and messages[-1]["role"] == "user":
                messages.pop()

    st.rerun()
