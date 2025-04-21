# main.py

import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import FastAPI, HTTPException, Body
from typing import Dict

app = FastAPI(
    title="Cyber Anomaly Detector API",
    description="Uploads one row of network‑flow features and returns BENIGN or ANOMALY",
)

BASE = os.path.dirname(__file__)
FEATURE_PATH = os.path.join(BASE, "models", "feature_names.json")
MODEL_PATH   = os.path.join(BASE, "models", "model_80.99.h5")
TH_PATH      = os.path.join(BASE, "models", "threshold.json")

# 1️⃣ Load artifacts once
if not os.path.exists(FEATURE_PATH):
    raise RuntimeError(f"Missing feature list: {FEATURE_PATH}")
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Missing model file:   {MODEL_PATH}")
if not os.path.exists(TH_PATH):
    raise RuntimeError(f"Missing threshold:    {TH_PATH}")

with open(FEATURE_PATH) as f:
    FEATURE_COLUMNS = json.load(f)
with open(TH_PATH) as f:
    THRESHOLD = json.load(f)["threshold"]

autoencoder = tf.keras.models.load_model(MODEL_PATH, compile=False)

@app.get("/")
def read_root():
    return {"message": "API up"}

@app.post("/predict")
def predict(data: Dict[str, float] = Body(...)):
    """
    Expects a flat JSON dict of { feature_name: value, ... }.
    """
    try:
        # 1) normalize into DataFrame
        df = pd.json_normalize(data)
        # 2) ensure exact ordering + fill missing
        df = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)
        # 3) to array & inference
        row = df.to_numpy().astype(np.float32)
        recon = autoencoder.predict(row, verbose=0)
        mse   = float(np.mean((row - recon)**2, axis=1)[0])
        label = "ANOMALY" if mse > THRESHOLD else "BENIGN"
        return {"label": label}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
