# Backend — API FastAPI

## Requisitos
- Python 3.10+
- `artifacts/model.joblib` generado por el notebook

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```
Variables opcionales:
- `MODEL_PATH` (ruta al modelo, default: `artifacts/model.joblib`)

## Endpoints
- `GET /health`
- `POST /predict` (JSON de una obra)
- `POST /predict-csv` (multipart/form-data con archivo CSV)
