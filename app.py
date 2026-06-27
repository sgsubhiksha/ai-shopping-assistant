import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="Shop Assistant", page_icon=None, layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: linear-gradient(90deg, #060912 0%, #0b1226 45%, #0a1830 100%);
        border-bottom: 0.5px solid #1c2c4a;
    }
    [data-testid="stToolbar"] {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background: linear-gradient(160deg, #05070d 0%, #070b16 35%, #0a1124 70%, #060911 100%);
    }

    .bg-blobs {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
        pointer-events: none;
    }
    .blob {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.35;
    }
    .blob-1 {
        width: 420px;
        height: 420px;
        background: radial-gradient(circle, #2a4fc0, transparent 70%);
        top: -120px;
        left: -100px;
    }
    .blob-2 {
        width: 360px;
        height: 360px;
        background: radial-gradient(circle, #1b3a8a, transparent 70%);
        top: 30%;
        right: -120px;
    }
    .blob-3 {
        width: 480px;
        height: 480px;
        background: radial-gradient(circle, #14224d, transparent 70%);
        bottom: -150px;
        left: 20%;
    }
    .blob-4 {
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, #3a6bcf, transparent 70%);
        bottom: 10%;
        right: 10%;
    }

    [data-testid="stChatInput"] {
        background: transparent;
        padding: 4px;
        border-radius: 999px;
        background-image: linear-gradient(120deg, #1b3a8a 0%, #3a6bcf 40%, #0a1124 100%);
        overflow: hidden;
    }
    [data-testid="stChatInput"] > div {
        border-radius: 999px;
        background: #060911;
        margin: 2px;
        overflow: hidden;
    }
    [data-testid="stChatInput"] > div > div {
        border-radius: 999px;
        overflow: hidden;
    }
    [data-baseweb="base-input"] {
        border-radius: 999px !important;
        overflow: hidden;
    }
    [data-testid="stChatInput"] textarea {
        border: none;
        border-radius: 999px;
        background: transparent;
        color: #e8ecf5;
        font-size: 15px;
        padding: 12px 20px;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #5a6c94;
    }
    [data-testid="stChatInput"]:has(textarea:focus) {
        background-image: linear-gradient(120deg, #2a4fc0 0%, #5d8cf0 40%, #1b3a8a 100%);
        box-shadow: 0 0 24px rgba(58, 107, 207, 0.35);
    }
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #3a6bcf, #1b3a8a);
        border-radius: 50%;
        border: none;
    }
    [data-testid="stChatInput"] button svg {
        fill: #e8ecf5;
    }
    [data-testid="stChatInput"] *,
    [data-testid="stChatInput"] *::before,
    [data-testid="stChatInput"] *::after {
        border-radius: 999px !important;
    }

    h1 {
        font-weight: 500;
        font-size: 22px;
        letter-spacing: -0.01em;
        background: linear-gradient(90deg, #cdd9f5, #88a6e8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .typewriter-box {
        min-height: 28px;
        font-size: 14px;
        color: #7d93c4;
        margin-top: 4px;
        margin-bottom: 2rem;
        font-family: var(--font-mono, monospace);
    }
    .cursor {
        display: inline-block;
        width: 7px;
        background: #5d83d8;
        margin-left: 2px;
        animation: blink 0.9s step-start infinite;
    }
    @keyframes blink { 50% { opacity: 0; } }

    .product-card {
        border: 0.5px solid #1c2c4a;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 8px;
        background: linear-gradient(135deg, #0b1020 0%, #0c1830 100%);
    }
    .product-name {
        font-weight: 500;
        font-size: 14px;
        color: #e8ecf5;
        margin: 0 0 4px 0;
    }
    .product-meta {
        font-size: 12px;
        color: #6b7da3;
        margin: 0;
    }
    .product-price {
        font-weight: 500;
        font-size: 14px;
        background: linear-gradient(90deg, #9db8f0, #6b8fe0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: right;
    }
    .divider-thin {
        border-top: 0.5px solid #1c2c4a;
        margin: 1.5rem 0;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #05070d 0%, #0a1124 100%);
        border-right: 0.5px solid #1c2c4a;
    }
    .stButton button {
        border: 0.5px solid #24365e;
        border-radius: 10px;
        background: linear-gradient(135deg, #0c1226, #0a1830);
        color: #cdd9f5;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #101a36, #0d2040);
        border-color: #3a6bcf;
    }
    .stMarkdown p {
        color: #c4cde3;
        line-height: 1.7;
    }
    [data-testid="stExpander"] {
        border: 0.5px solid #1c2c4a;
        border-radius: 10px;
        background: #0b1020;
    }
</style>
<div class="bg-blobs">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>
    <div class="blob blob-4"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1>Shop assistant</h1>", unsafe_allow_html=True)

components.html("""
<style>
    body {
        margin: 0;
        background: transparent;
        font-family: -apple-system, sans-serif;
    }
    .typewriter-box {
        min-height: 28px;
        font-size: 14px;
        color: #7d93c4;
        font-family: monospace;
    }
    .cursor {
        display: inline-block;
        width: 7px;
        background: #5d83d8;
        margin-left: 2px;
        animation: blink 0.9s step-start infinite;
    }
    @keyframes blink { 50% { opacity: 0; } }
</style>
<div class="typewriter-box"><span id="tw-text"></span><span class="cursor"></span></div>
<script>
const lines = [
    "What are you looking for today?",
    "Ask me anything about the catalog.",
    "Try: running shoes under 2000.",
    "I remember context. Ask follow-ups freely."
];
let lineIndex = 0;
let charIndex = 0;
let deleting = false;

function tick() {
    const el = document.getElementById("tw-text");
    if (!el) return;
    const current = lines[lineIndex];

    if (!deleting) {
        charIndex++;
        el.textContent = current.slice(0, charIndex);
        if (charIndex === current.length) {
            deleting = true;
            setTimeout(tick, 5000);
            return;
        }
        setTimeout(tick, 45);
    } else {
        charIndex--;
        el.textContent = current.slice(0, charIndex);
        if (charIndex === 0) {
            deleting = false;
            lineIndex = (lineIndex + 1) % lines.length;
            setTimeout(tick, 300);
            return;
        }
        setTimeout(tick, 25);
    }
}
tick();
</script>
""", height=40)

API_URL = "http://127.0.0.1:8000/search"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=None):
        st.markdown(msg["content"])

if query := st.chat_input("Running shoes under 2000"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar=None):
        st.markdown(query)

    with st.chat_message("assistant", avatar=None):
        with st.spinner("Searching"):
            try:
                history = st.session_state.messages[:-1]

                response = requests.post(API_URL, json={
                    "query": query,
                    "top_k": 5,
                    "history": history
                })
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                products = data["products"]

                st.markdown(answer)

                if products:
                    st.markdown("<div class='divider-thin'></div>", unsafe_allow_html=True)
                    for p in products:
                        st.markdown(f"""
                        <div class="product-card">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <div>
                                    <p class="product-name">{p['product_name'][:55]}</p>
                                    <p class="product-meta">{p['brand']} · {p['main_category']}</p>
                                </div>
                                <div class="product-price">Rs {p['discounted_price']:.0f}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                error_msg = f"Connection error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

with st.sidebar:
    st.markdown("<p style='color:#6b7da3; font-size:13px; letter-spacing:0.02em;'>RAG · FAISS · LLAMA 3.1</p>", unsafe_allow_html=True)
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()