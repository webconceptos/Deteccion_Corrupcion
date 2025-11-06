import json

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.api.deps import get_model_and_meta
from src.api.routes.health import router as health_router
from src.api.schemas import BatchPredictRequest, PredictBatchResponse, PredictResponse

app = FastAPI(title="Detección de Riesgos de Corrupción", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)

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


@app.post("/predict_proba", response_model=PredictBatchResponse, tags=["predict"])
def predict_proba(req: BatchPredictRequest):
    pipeline, meta = get_model_and_meta()

    cols_meta = meta.get("columns")
    threshold = float(meta.get("best_threshold_f1", 0.5))
    if not cols_meta or not isinstance(cols_meta, list):
        raise HTTPException(status_code=500, detail="Meta sin columnas válidas.")

    # Alinear columnas: faltantes -> NaN; extras -> se ignoran
    aligned = []
    for i, row in enumerate(req.filas):
        aligned.append({c: row.get(c, None) for c in cols_meta})

    X = pd.DataFrame(aligned)[cols_meta]
    try:
        probas = pipeline.predict_proba(X)[:, 1]
    except AttributeError:
        # Si es un pipeline de decision_function:
        scores = pipeline.decision_function(X)
        probas = (scores - scores.min()) / (scores.max() - scores.min() + 1e-9)

    resultados = []
    for p in probas:
        resultados.append(
            PredictResponse(
                proba=float(p),
                threshold=threshold,
                riesgoso=bool(p >= threshold),
            )
        )
    return PredictBatchResponse(resultados=resultados)


@app.post("/predict_batch")
def predict_batch(payload: list[dict]):
    import pandas as pd

    X = pd.DataFrame(payload)
    probas = pipe.predict_proba(X)[:, 1]
    labels = (probas >= THR).astype(int)
    return {"probas": probas.tolist(), "labels": labels.tolist(), "threshold": THR}
