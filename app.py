# app.py

import os
import json
import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf

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

# ─── 3️⃣ Load feature names, model, threshold ─────────────
FEATURE_PATH = "models/feature_names.json"
MODEL_PATH   = "models/autoencoder.h5"
TH_PATH      = "models/threshold.json"

# Load feature list
if not os.path.exists(FEATURE_PATH):
    st.error(f"Missing {FEATURE_PATH}. Run your notebook to save feature_names.json.")
    st.stop()
FEATURE_COLUMNS = json.load(open(FEATURE_PATH))

@st.cache_resource
def load_model_and_threshold():
    # Ensure all required files exist
    missing = [p for p in (MODEL_PATH, TH_PATH) if not os.path.exists(p)]
    if missing:
        st.error(
            "Missing files:\n" +
            "\n".join(f"- {m}" for m in missing) +
            "\n\nMake sure your notebook saved autoencoder.h5 and threshold.json."
        )
        st.stop()

    # Skip compiling (we only need inference)
    ae = tf.keras.models.load_model(MODEL_PATH, compile=False)
    threshold = json.load(open(TH_PATH))["threshold"]
    return ae, threshold

autoencoder, THRESHOLD = load_model_and_threshold()

# ─── 4️⃣ Inference helper ─────────────────────────────────
def classify(data: dict):
    df = pd.json_normalize(data)
    # Reindex to exactly the columns we trained on, filling missing with 0
    df = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)
    row = df.to_numpy().astype(np.float32)  # shape (1, 62)

    recon = autoencoder.predict(row, verbose=0)
    mse   = float(np.mean((row - recon) ** 2, axis=1)[0])
    label = "ANOMALY" if mse > THRESHOLD else "BENIGN"
    return label, mse

# ─── 5️⃣ Page navigation ─────────────────────────────────
page = st.sidebar.radio("📂 Navigate", ["Home", "Team"])

# ─── 6️⃣ Home: anomaly test UI ───────────────────────────
if page == "Home":
    st.markdown('<div class="console">', unsafe_allow_html=True)
    st.markdown('<div class="neon-title">> Anomaly Detector Test</div>', unsafe_allow_html=True)

    st.write("""
    Upload a single **row JSON** matching your dataset schema,  
    and the autoencoder will reconstruct it. We flag it  
    as **ANOMALY** if its reconstruction MSE exceeds the threshold.
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="neon-box">', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload your row JSON", type=["json"])
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded:
        data = json.load(uploaded)
        st.subheader("📄 Input JSON")
        st.json(data)

        try:
            label, mse = classify(data)
            st.markdown('<div class="neon-box">', unsafe_allow_html=True)
            st.markdown(f"### 🔍 Label: **{label}**")
            st.write(f"- Reconstruction MSE: `{mse:.6f}`")
            st.write(f"- Threshold:          `{THRESHOLD:.6f}`")
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❗ Error running model: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ─── 7️⃣ Team page ───────────────────────────────────────
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
