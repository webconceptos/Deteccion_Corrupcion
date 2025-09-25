import json, joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
pipe = joblib.load("models/pipeline.pkl")
meta = json.load(open("models/pipeline_meta.json"))
THR = meta.get("best_threshold_f1", 0.5)

class Item(BaseModel):
    # incluye aquí las columnas que espera el pipeline
    # ejemplo:
    SECTOR: str | None = None
    # ...
    # (o usa dict[str, Any] si vas a pasar variable el esquema)
    pass

@app.post("/predict_proba")
def predict_proba(payload: dict):
    X = [payload]  # una fila
    proba = pipe.predict_proba(X)[0][1]
    return {"proba": float(proba), "threshold": THR, "riesgoso": proba >= THR}

@app.post("/predict_batch")
def predict_batch(payload: list[dict]):
    import pandas as pd
    X = pd.DataFrame(payload)
    probas = pipe.predict_proba(X)[:, 1]
    labels = (probas >= THR).astype(int)
    return {"probas": probas.tolist(), "labels": labels.tolist(), "threshold": THR}
