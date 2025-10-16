import io
import os

import joblib
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/model.joblib")

app = FastAPI(title="API Riesgo Corrupción Obras")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carga perezosa del modelo
_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


# ---- ETL/flags: replicar las banderas del notebook ----
def add_flags(df: pd.DataFrame) -> pd.DataFrame:
    if "adicionales_pct" in df.columns:
        df["flag_adicionales_altos"] = (df["adicionales_pct"] > 0.15).astype(int)
    if "ampliaciones" in df.columns:
        df["flag_muchas_ampliaciones"] = (df["ampliaciones"] >= 2).astype(int)
    if "penalidades" in df.columns:
        df["flag_penalidades"] = (df["penalidades"] >= 1).astype(int)
    if "tipo_proceso" in df.columns:
        df["flag_contratacion_directa"] = (df["tipo_proceso"] == "Contratación Directa").astype(int)
    if "region_riesgo" in df.columns:
        df["flag_region_alta"] = (df["region_riesgo"] == "ALTA").astype(int)
    return df


class ObraIn(BaseModel):
    costo_total: float
    plazo_meses: int
    adicionales_pct: float
    ampliaciones: int
    penalidades: int
    baja_competencia: int
    empresa_sancionada: int
    consorcio: int
    experiencia_entidad: int
    region_riesgo: str
    tipo_proceso: str


@app.get("/health")
def health():
    try:
        m = get_model()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/predict")
def predict(item: ObraIn):
    df = pd.DataFrame([item.dict()])
    df = add_flags(df)
    model = get_model()
    proba = model.predict_proba(df)[:, 1]
    pred = (proba >= 0.5).astype(int)
    # Sugerir "flags" activados
    flags = []
    if df.get("flag_adicionales_altos") is not None and int(df["flag_adicionales_altos"][0]) == 1:
        flags.append("Adicionales > 15%")
    if (
        df.get("flag_muchas_ampliaciones") is not None
        and int(df["flag_muchas_ampliaciones"][0]) == 1
    ):
        flags.append(">= 2 Ampliaciones")
    if df.get("flag_penalidades") is not None and int(df["flag_penalidades"][0]) == 1:
        flags.append("Penalidades registradas")
    if (
        df.get("flag_contratacion_directa") is not None
        and int(df["flag_contratacion_directa"][0]) == 1
    ):
        flags.append("Contratación Directa")
    if df.get("flag_region_alta") is not None and int(df["flag_region_alta"][0]) == 1:
        flags.append("Región de riesgo ALTA")

    return {"prob_riesgo": float(proba[0]), "pred_riesgo": int(pred[0]), "top_flags": flags}


@app.post("/predict-csv")
async def predict_csv(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    df = add_flags(df.copy())
    model = get_model()
    proba = model.predict_proba(df)[:, 1]
    pred = (proba >= 0.5).astype(int)
    out = df.copy()
    out["prob_riesgo"] = proba
    out["pred_riesgo"] = pred
    # Devolver JSON compacto
    return {"rows": out.to_dict(orient="records"), "count": len(out)}
