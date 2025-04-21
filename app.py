# app.py

import streamlit as st
import json
import requests

# ─── 1️⃣ Page config ─────────────────────────────────
st.set_page_config(
    page_title="Cyber Classifier",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── 2️⃣ Inline CSS ───────────────────────────────────
st.markdown("""
<style>
  /* Full‑screen animated background + dark overlay */
  [data-testid="stAppViewContainer"] {
    background: url("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMG45YmdmN2E2Zm0wMnZjdGU3OXpkOXpkdms0ZGN3eDdlNnUxZ3YzNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9WC8WTZsFxkRi/giphy.gif")
      center/cover no-repeat fixed;
  }
  [data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.7);
    z-index: 0;
  }

  /* central “console” panel */
  .console {
    max-width: 900px;
    margin: 3rem auto;
    padding: 2rem;
    background: rgba(0,0,0,0.5);
    border: 1px solid #39ff14;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(57,255,20,0.6);
    position: relative; z-index: 1;
  }

  /* glitchy neon heading */
  @keyframes glitch {
    0%,100% { text-shadow: 2px 2px #00ff00, -2px -2px #00ff00; }
    25%     { text-shadow: -2px 2px #39ff14, 2px -2px #39ff14; }
    50%     { text-shadow: 2px -2px #00ff00, -2px 2px #00ff00; }
    75%     { text-shadow: -2px -2px #39ff14, 2px 2px #39ff14; }
  }
  .neon-title {
    font-family: 'Courier New', monospace;
    color: #39ff14;
    font-size: 3rem;
    animation: glitch 1s infinite;
    margin-bottom: 0.5rem;
    text-align: center;
  }

  /* neon‑box wrapper */
  .neon-box {
    border: 2px solid #39ff14;
    border-radius: 8px;
    padding: 1rem;
    margin: 1.5rem 0;
    background: rgba(0,0,0,0.6);
    box-shadow: inset 0 0 10px #39ff14;
  }

  /* horizontal rule in green */
  hr {
    border-top: 1px solid #39ff14;
    margin: 2rem 0;
  }

  /* Team cards: fixed height + flex centering */
  .team-card {
    background: rgba(0,0,0,0.6);
    border: 2px solid #39ff14;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem;
    box-shadow: 0 0 10px #39ff14;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    height: 130px;
    box-sizing: border-box;
  }
</style>
""", unsafe_allow_html=True)

# ─── 3️⃣ Page navigation ─────────────────────────────────
page = st.sidebar.radio("📂 Navigate", ["Home", "Team"])

# ─── 4️⃣ Home: call the FastAPI for inference ───────────
if page == "Home":
    st.markdown('<div class="console">', unsafe_allow_html=True)
    st.markdown('<div class="neon-title">> Cyber Anomaly Test</div>', unsafe_allow_html=True)

    st.write("""
    Upload a single **row JSON** matching your dataset schema,  
    and see **BENIGN** or **ANOMALY** via our FastAPI service.
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="neon-box">', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload your row JSON", type=["json"])
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded:
        # load raw JSON
        raw = json.load(uploaded)

        # if it’s a list, grab the first element
        if isinstance(raw, list) and raw:
            payload = raw[0]
        else:
            payload = raw

        # call FastAPI
        try:
            res = requests.post(
                "http://localhost:8000/predict",
                json=payload,
                timeout=5
            )
            res.raise_for_status()
            label = res.json().get("label", "ERROR")
        except Exception as e:
            st.error(f"❗ API error: {e}")
            label = None

        # display result
        if label:
            st.markdown('<div class="neon-box">', unsafe_allow_html=True)
            st.markdown(f"### 🔍 Label: **{label}**", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─── 5️⃣ Team page (unchanged) ───────────────────────────
else:
    st.markdown('<div class="console">', unsafe_allow_html=True)
    st.markdown('<div class="neon-title">> Meet the Team</div>', unsafe_allow_html=True)
    st.write("Our cyber‑security sheriffs behind the scenes:")

    team = [
        ("Yousef Al‑Dayhani",   "Backend Developer"),
        ("Alhanouf Al‑Suwaid",  "Backend Developer"),
        ("Ezdhar Al‑Tamimi",    "Backend Developer"),
        ("Rahaf Masmali",       "Backend Developer"),
        ("Omar Al‑Suraia",      "Backend Developer"),
    ]

    cols = st.columns(5, gap="small")
    for col, (name, role) in zip(cols, team):
        with col:
            st.markdown(f"""
                <div class="team-card">
                  <h4>{name}</h4>
                  <p><em>{role}</em></p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
