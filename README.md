# Tesis: Detección de Riesgos de Corrupción en Obras Públicas (Starter)

Este repositorio inicial está listo para:
- Ingesta y unificación de datos (SEACE, SIAF, Invierte.pe, INFOBRAS, RNP, informes).
- Preparación de *datasets* etiquetados para ML.
- Entrenamiento de modelos base (Regresión Logística, RandomForest, XGBoost/LightGBM).
- Interpretabilidad (XAI) con SHAP.
- Exposición del modelo vía FastAPI.
- Trazabilidad & MLOps (MLflow básico).

## Estructura
```
tesis-corrupcion-ml-starter/
├── data/               # raw, external, interim, processed
├── models/             # artefactos de modelos (.pkl)
├── notebooks/          # notebooks de EDA y prototipos
├── reports/figures/    # gráficos exportados
├── src/
│   ├── api/            # FastAPI para inferencia
│   ├── config/         # gestión de variables de entorno
│   ├── data/           # ingesta, validación, firma de esquemas
│   ├── features/       # ingeniería de variables
│   ├── models/         # entrenamiento, evaluación, persistencia
│   └── utils/          # logging, helpers
├── tests/              # pruebas unitarias (pytest)
├── requirements.txt
├── .env.example
└── README.md
```

## Rutas locales de tus archivos actuales
Coloca aquí copias o enlaces simbólicos de tus fuentes (si procede). En este entorno he detectado algunos archivos que ya subiste (carpeta `/mnt/data`):
- 1.HI N°000001-2021-CG-SFI-LAS.pdf
- 05.1 Entregable subsanado.pdf
- Trabajo Finla de Proy investigacion I-ultimo.pptx
- Perfilamiento Obra Riesgosa_CATEGORÍA X_2023.05.12.xlsx
- Perfilamiento de Empresa riesgosa_ CATEGORÍA X _2023.05.12.xlsx
- Perfilamiento de Funcionario riesgoso_ CATEGORÍA X _2023.05.12.xlsx
- Diccionario_Datos_ML_Completo_V1.xlsx
- Diccionario_Datos_Sistemas_Fuente_V1.xlsx

> Recomendación: copia los Excel de diccionarios a `data/external/` y las extracciones crudas a `data/raw/`.

## Instalación rápida
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # y configura credenciales
```

## Entrenamiento rápido (baseline)
```bash
python -m src.models.train --input data/processed/dataset_obras.parquet   --target y_riesgo --model rf --out models/rf_baseline.pkl
```

## API de inferencia (FastAPI)
```bash
uvicorn src.api.main:app --reload --port 8080
```

## MLflow (opcional)
```bash
mlflow ui --port 5000 --backend-store-uri mlruns
```
