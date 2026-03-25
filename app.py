# app.py
import streamlit as st
from document_loader import load_documents, load_uploaded_file
from search_engine import search_documents
from answer_generator import generate_answer

st.set_page_config(
    page_title="Dobby AI",
    page_icon="🧦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background-color: #0e0b07;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(139, 90, 20, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(74, 40, 10, 0.2) 0%, transparent 50%);
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Fix the scroll issue - remove all top padding */
[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0804 0%, #120e06 40%, #0d0a05 100%) !important;
    border-right: 1px solid rgba(212, 168, 67, 0.2) !important;
}

[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem !important;
}

.sidebar-logo {
    text-align: center;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(212, 168, 67, 0.25);
    margin-bottom: 1.2rem;
}

.sidebar-logo-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 0.4rem;
}

.sidebar-logo-text {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #d4a843;
    letter-spacing: 0.15em;
}

.sidebar-logo-sub {
    font-family: 'Crimson Text', serif;
    font-size: 0.8rem;
    color: rgba(212, 168, 67, 0.5);
    font-style: italic;
    margin-top: 0.2rem;
}

.sidebar-stat {
    background: rgba(212, 168, 67, 0.07);
    border: 1px solid rgba(212, 168, 67, 0.15);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.5rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: rgba(212, 168, 67, 0.7);
    display: flex;
    justify-content: space-between;
}

.sidebar-stat span:last-child {
    color: #d4a843;
    font-weight: 500;
}

.sidebar-section-title {
    font-family: 'Cinzel', serif;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: rgba(212, 168, 67, 0.45);
    text-transform: uppercase;
    margin: 1.2rem 0 0.7rem;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: transparent !important;
    border: 1px solid rgba(212, 168, 67, 0.25) !important;
    color: rgba(212, 168, 67, 0.6) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    padding: 0.5rem !important;
    margin-top: 0.4rem !important;
    transition: all 0.2s !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(212, 168, 67, 0.1) !important;
    border-color: rgba(212, 168, 67, 0.5) !important;
    color: #d4a843 !important;
}

/* ── Mobile upload bar (shown only on mobile) ── */
.mobile-upload-bar {
    display: none;
    background: rgba(15, 11, 5, 0.95);
    border-bottom: 1px solid rgba(212, 168, 67, 0.15);
    padding: 0.6rem 1rem;
    position: sticky;
    top: 0;
    z-index: 999;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.mobile-upload-bar-title {
    font-family: 'Cinzel', serif;
    font-size: 0.9rem;
    color: #d4a843;
    white-space: nowrap;
}

@media (max-width: 768px) {
    .mobile-upload-bar { display: flex; }
}

/* ── Main header ── */
.chat-header {
    padding: 1.2rem 1rem 1rem;
    text-align: center;
    border-bottom: 1px solid rgba(212, 168, 67, 0.12);
}

.chat-header-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(1.4rem, 4vw, 2rem);
    font-weight: 700;
    color: #d4a843;
    letter-spacing: 0.1em;
    text-shadow: 0 0 30px rgba(212, 168, 67, 0.3);
}

.chat-header-sub {
    font-family: 'Crimson Text', serif;
    font-style: italic;
    font-size: clamp(0.8rem, 2.5vw, 0.95rem);
    color: rgba(200, 170, 100, 0.5);
    margin-top: 0.2rem;
}

/* ── Messages ── */
.msg-row {
    display: flex;
    margin-bottom: 1rem;
    align-items: flex-end;
    gap: 8px;
    padding: 0 1rem;
}

.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}

.avatar-dobby {
    background: radial-gradient(circle, rgba(80,140,80,0.4), rgba(40,80,40,0.6));
    border: 1px solid rgba(100, 180, 100, 0.3);
}

.avatar-user {
    background: radial-gradient(circle, rgba(180,130,40,0.4), rgba(120,80,20,0.6));
    border: 1px solid rgba(212, 168, 67, 0.3);
}

.bubble {
    max-width: min(72%, 600px);
    padding: 0.75rem 1rem;
    border-radius: 18px;
    font-family: 'Crimson Text', serif;
    font-size: clamp(0.95rem, 2.5vw, 1.05rem);
    line-height: 1.65;
}

.bubble-dobby {
    background: linear-gradient(135deg, rgba(25,45,25,0.85), rgba(20,38,20,0.9));
    border: 1px solid rgba(100, 180, 100, 0.2);
    border-bottom-left-radius: 4px;
    color: #d4ebd4;
}

.bubble-user {
    background: linear-gradient(135deg, rgba(100,65,15,0.7), rgba(80,50,10,0.8));
    border: 1px solid rgba(212, 168, 67, 0.25);
    border-bottom-right-radius: 4px;
    color: #f0dfa8;
}

.source-pill {
    display: inline-block;
    margin-top: 0.5rem;
    padding: 0.2rem 0.7rem;
    background: rgba(212, 168, 67, 0.1);
    border: 1px solid rgba(212, 168, 67, 0.25);
    border-radius: 20px;
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    color: rgba(212, 168, 67, 0.7);
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    opacity: 0.5;
}

.empty-state-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }

.empty-state-text {
    font-family: 'Crimson Text', serif;
    font-style: italic;
    font-size: clamp(0.95rem, 2.5vw, 1.1rem);
    color: rgba(212, 168, 67, 0.6);
    line-height: 1.6;
}

/* ── Input area ── */
.input-wrapper {
    position: sticky;
    bottom: 0;
    background: linear-gradient(to top, #0e0b07 80%, transparent);
    padding: 0.8rem 1rem 1.2rem;
    border-top: 1px solid rgba(212, 168, 67, 0.1);
}

.stTextInput > div > div > input {
    background: rgba(20, 15, 5, 0.9) !important;
    border: 1px solid rgba(212, 168, 67, 0.3) !important;
    border-radius: 14px !important;
    color: #f0e6d3 !important;
    font-family: 'Crimson Text', serif !important;
    font-size: clamp(0.95rem, 2.5vw, 1rem) !important;
    padding: 0.7rem 1rem !important;
    caret-color: #d4a843 !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(212, 168, 67, 0.3) !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(212, 168, 67, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(212, 168, 67, 0.08) !important;
    outline: none !important;
}

/* ── Send button ── */
.send-btn .stButton > button {
    background: linear-gradient(135deg, #8b5a14, #d4a843) !important;
    color: #0e0b07 !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    padding: 0.7rem 1rem !important;
    width: 100% !important;
    box-shadow: 0 4px 15px rgba(212, 168, 67, 0.25) !important;
    transition: all 0.2s !important;
}

.send-btn .stButton > button:hover {
    box-shadow: 0 4px 25px rgba(212, 168, 67, 0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(212, 168, 67, 0.2);
    border-radius: 2px;
}

/* ── Mobile tweaks ── */
@media (max-width: 768px) {
    .msg-row { padding: 0 0.5rem; }
    .bubble { max-width: 85%; }
    .chat-header { padding: 0.8rem 0.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Load documents ──
@st.cache_resource
def load_base_docs():
    return load_documents("documents")

base_docs = load_base_docs()

# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

all_docs = base_docs + st.session_state.uploaded_docs

# ════════════════════════════════
# SIDEBAR
# ════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-logo-icon">🧦</span>
        <div class="sidebar-logo-text">DOBBY AI</div>
        <div class="sidebar-logo-sub">Your magical study companion</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-stat">
        <span>📚 Documents</span><span>{len(all_docs)}</span>
    </div>
    <div class="sidebar-stat">
        <span>💬 Messages</span><span>{len(st.session_state.messages)}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">📎 Upload Scroll</div>', unsafe_allow_html=True)
    uploaded_side = st.file_uploader("", type=["pdf", "txt"], label_visibility="collapsed", key="sidebar_upload")
    if uploaded_side:
        new_doc = load_uploaded_file(uploaded_side)
        if new_doc and new_doc["source"] not in [d["source"] for d in st.session_state.uploaded_docs]:
            st.session_state.uploaded_docs.append(new_doc)
            st.success(f"✨ {new_doc['source']} added!")

    st.markdown('<div class="sidebar-section-title">⚙️ Actions</div>', unsafe_allow_html=True)
    if st.button("🗑️ Vanish Chat History"):
        st.session_state.messages = []
        st.rerun()

# ════════════════════════════════
# MOBILE TOP BAR — upload visible on phone
# ════════════════════════════════
st.markdown("""
<div class="mobile-upload-bar">
    <span class="mobile-upload-bar-title">🧦 Dobby AI</span>
</div>
""", unsafe_allow_html=True)

# Mobile upload expander — only visible on small screens
with st.expander("📎 Upload a document (mobile)", expanded=False):
    uploaded_mobile = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"],
        key="mobile_upload"
    )
    if uploaded_mobile:
        new_doc = load_uploaded_file(uploaded_mobile)
        if new_doc and new_doc["source"] not in [d["source"] for d in st.session_state.uploaded_docs]:
            st.session_state.uploaded_docs.append(new_doc)
            st.success(f"✨ {new_doc['source']} added!")

# ════════════════════════════════
# MAIN CHAT
# ════════════════════════════════
st.markdown("""
<div class="chat-header">
    <div class="chat-header-title">🧦 Dobby AI</div>
    <div class="chat-header-sub">Ask and Dobby shall answer, Master</div>
</div>
""", unsafe_allow_html=True)

# Messages
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">✨</div>
        <div class="empty-state-text">
            Dobby is waiting for your question, Master...<br>
            <small style="font-size:0.85rem; opacity:0.7">Upload a scroll and cast your question below</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user">
                <div class="avatar avatar-user">🧙</div>
                <div class="bubble bubble-user">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            sources_html = ""
            if msg.get("sources"):
                sources_html = f'<div><span class="source-pill">📄 {" · ".join(msg["sources"])}</span></div>'
            st.markdown(f"""
            <div class="msg-row">
                <div class="avatar avatar-dobby">🧦</div>
                <div class="bubble bubble-dobby">
                    {msg['content']}
                    {sources_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Input ──
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "",
        placeholder="Cast your question here, Master...",
        label_visibility="collapsed",
        key="chat_input"
    )

with col2:
    st.markdown('<div class="send-btn">', unsafe_allow_html=True)
    send = st.button("✦ Accio", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Handle send ──
if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("🧦 Dobby is thinking..."):
        context = search_documents(user_input, all_docs)
        answer, sources = generate_answer(
            user_input,
            context,
            st.session_state.messages[:-1]
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })

    st.rerun()