from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from pathlib import Path
import os

app = FastAPI(title='Riesgo Corrupción Obras Públicas - API')

MODEL_PATH = Path(os.getenv('MODEL_PATH', 'models/rf_baseline.pkl'))
_model = None

class ObraRequest(BaseModel):
    # Agregar aquí los principales features que use el modelo (ejemplos)
    valor_referencial: float | None = None
    plazo_meses: float | None = None
    nro_participantes: int | None = None
    tipo_contratacion: str | None = None

def load_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    return _model

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/predict')
def predict(item: ObraRequest):
    model = load_model()
    if model is None:
        return {'error': f'Modelo no encontrado en {MODEL_PATH}'}
    # Construir vector en el mismo orden que el entrenamiento (ejemplo simple)
    # En producción, usar un preprocesador persistido (OneHotEncoder/ColumnTransformer, etc.)
    features = [[
        item.valor_referencial or 0.0,
        item.plazo_meses or 0.0,
        item.nro_participantes or 0,
    ]]
    pred = model.predict(features)[0]
    return {'riesgo': int(pred)}
