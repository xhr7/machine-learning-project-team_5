# main.py

import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from fastapi import FastAPI, HTTPException, Body
from typing import Dict

app = FastAPI(
    title="Cyber Anomaly Detector API",
    description="Detect BENIGN vs. ANOMALY; if ANOMALY, classify attack type",
)

# ─── Paths ──────────────────────────────────────────────
BASE         = os.path.dirname(__file__)
FEATURE_PATH = os.path.join(BASE, "models", "feature_names.json")
AE_MODEL     = os.path.join(BASE, "models", "model_80.99.h5")
THRESH_PATH  = os.path.join(BASE, "models", "threshold.json")
DT_MODEL     = os.path.join(BASE, "models", "decision_tree_model.pkl")
LE_PATH      = os.path.join(BASE, "models", "label_encoder.pkl")

# ─── Load once at startup ─────────────────────────────────
if not os.path.exists(FEATURE_PATH):
    raise RuntimeError(f"Missing feature list: {FEATURE_PATH}")
if not os.path.exists(AE_MODEL):
    raise RuntimeError(f"Missing autoencoder: {AE_MODEL}")
if not os.path.exists(THRESH_PATH):
    raise RuntimeError(f"Missing threshold: {THRESH_PATH}")
if not os.path.exists(DT_MODEL):
    raise RuntimeError(f"Missing Decision Tree model: {DT_MODEL}")
if not os.path.exists(LE_PATH):
    raise RuntimeError(f"Missing LabelEncoder: {LE_PATH}")

# 1) feature names & threshold
with open(FEATURE_PATH) as f:
    FEATURE_COLUMNS = json.load(f)
with open(THRESH_PATH) as f:
    THRESHOLD = json.load(f)["threshold"]

# 2) autoencoder
autoencoder = tf.keras.models.load_model(AE_MODEL, compile=False)

# 3) decision tree + label encoder
dt_model      = joblib.load(DT_MODEL)
label_encoder = joblib.load(LE_PATH)


@app.get("/")
def healthcheck():
    return {"message": "API up and running"}


@app.post("/predict")
def predict(data: Dict[str, float] = Body(...)):
    """
    Expects a flat JSON dict of { feature_name: value, ... }.
    Returns:
      - {"label":"BENIGN"} 
      - or {"label":"ANOMALY","attack":"DoS Hulk"}
    """
    try:
        # 1) normalize + align columns
        df = pd.json_normalize(data)
        df = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)
        row = df.to_numpy().astype(np.float32)

        # 2) autoencoder inference
        recon = autoencoder.predict(row, verbose=0)
        mse   = float(np.mean((row - recon) ** 2, axis=1)[0])

        # 3) decide BENIGN vs ANOMALY
        if mse <= THRESHOLD:
            return {"label": "BENIGN"}

        # 4) if ANOMALY, run second model
        pred_enc   = dt_model.predict(row)[0]
        attack_str = label_encoder.inverse_transform([pred_enc])[0]
        return {"label": "ANOMALY", "attack": attack_str}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
