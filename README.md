# Detección de Riesgos de Corrupción en Obras Públicas (Perú)

Sistema de **Machine Learning** que integra señales de **obra**, **empresa** y **miembro de comité** y etiqueta con la **Matriz de Priorización** para clasificar obras como **riesgosas (1)** o **no riesgosas (0)**.

### Curso : Proyecto de Investigación II
#### Integrantes: 
    Hilario Aradiel
    García Fernando
---

## Estructura del repositorio

```
DETECCION_CORRUPCION/
├─ data/
│  ├─ raw/                  # datos fuente (solo lectura)
│  ├─ interim/              # intermedios/temporales
│  ├─ processed/            # dataset final para modelado (parquet)
│  └─ external/             # fuentes externas (si aplica)
├─ models/
│  ├─ pipeline.pkl          # pipeline sklearn (preprocesamiento + modelo)
│  └─ pipeline_meta.json    # metadatos (columnas, umbral, scores CV)
├─ notebooks/
│  ├─ 01_exploracion_diccionarios.ipynb
│  ├─ 02_construir_dataset_maestro_final.ipynb
│  ├─ 03_entrenamiento_evaluacion_final.ipynb
│  └─ EDA_baseline.ipynb
├─ reports/
│  └─ figures/
│     ├─ 01_target_dist.png
│     ├─ 02_missing_top20.png
│     ├─ 03_importance_perm.png
│     ├─ 04_corr_heatmap.png
│     └─ 05_top_categorias.png
├─ scripts/
│  ├─ ingest.py             # ingesta con hash y logging
│  └─ preprocess.py         # limpieza mínima y verificación de processed
├─ src/
│  ├─ api/                  # FastAPI para servir el modelo
│  ├─ config/ data/ features/ models/ utils/  # módulos auxiliares
├─ tests/
├─ .env / .env.example
├─ README.md
└─ requirements.txt
```

---

## Objetivo

- **Problema:** identificar **obras con riesgo de corrupción** a partir de información administrativa y de ejecución.
- **Target:** `y_riesgo` (binario). En la versión actual se deriva principalmente de `OBRA_RIESGO` / `OBRA_RIESGO_DESC` (Matriz 1A/2A/3A) tras normalizar llaves (`CODIGO_UNICO` ↔ `COD_UNICO`/`CODIGO_OBRA`/`IDENTIFICADOR_OBRA`).
- **Dataset actual:** `data/processed/dataset_obras.parquet`.

---

## Reproducibilidad

### 1) Ingesta (copia a `data/raw/` + hash + log)
```bash
python scripts/ingest.py "C:/ruta/DS_DASH_Obra_1A.csv"
# salida: data/datasets.json (registro) y logs/ingest.log
```

### 2) Preprocesamiento mínimo (verificación y limpieza básica)
```bash
python scripts/preprocess.py
# salida: data/processed/dataset_obras.parquet y logs/preprocess.log
```

### 3) Construcción del dataset maestro
Ejecutar notebooks en orden:

1. `01_exploracion_diccionarios.ipynb` – mapeo/estandarización de campos.  
2. `02_construir_dataset_maestro_final.ipynb` – unión Obra+Empresa+Miembro, etiquetado desde Matriz, limpieza y export a parquet (`dataset_obras.parquet`).  
3. `EDA_baseline.ipynb` – genera figuras en `reports/figures/`.

### 4) Entrenamiento y evaluación
`03_entrenamiento_evaluacion_final.ipynb` compara modelos (**LogReg / RandomForest / GradientBoosting**) con **PR-AUC CV (5 folds)**, calcula **umbral óptimo por F1**, y guarda:

- `models/pipeline.pkl`  
- `models/pipeline_meta.json` (columnas, PR-AUC por modelo, `best_threshold_f1`)

---

## Métricas y gráficos

- **Validación:** **PR-AUC** (adecuada para desbalance), además de ROC-AUC y `classification_report`.
- **Holdout:** 80/20 estratificado.
- **Figuras generadas** (ver `reports/figures/`):
  - `01_target_dist.png` – distribución del target.  
  - `02_missing_top20.png` – nulos por columna (Top 20).  
  - `03_importance_perm.png` – *permutation importance* (índices transformados).  
  - `04_corr_heatmap.png` – matriz de correlación numérica.  
  - `05_top_categorias.png` – top categorías (ej. `SECTOR`).

---

## 🚀 API (serving)

Ejecuta la API con **FastAPI** (en `src/api/`):

```bash
uvicorn src.api.main:app --reload
```

- `POST /predict_proba` → `{ proba, threshold, riesgoso }`
  - Usa `models/pipeline.pkl` y `best_threshold_f1` de `models/pipeline_meta.json`.
- Importante: el JSON de entrada debe incluir **las mismas columnas** que espera el pipeline (nombres como en el parquet).

---

## ⚙️ Entorno

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

Variables opcionales en `.env` (ver `.env.example`).

---

## 📓 Notas de datos

- **Claves:**  
  - Obra: `CODIGO_UNICO` (variantes: `CODIGO_OBRA`, `IDENTIFICADOR_OBRA`).  
  - Matriz: `COD_UNICO` / `CODIGO_OBRA` / `IDENTIFICADOR_OBRA`.  
  - Empresa: `codigo_ruc`.  
  - Miembro: `codigo_dni`.

- **Prevención de fuga (leakage):** del entrenamiento se excluyen `OBRA_RIESGO`, `OBRA_RIESGO_DESC`, `PROYECTO_RIESGO`, `PROYECTO_RIESGO_DESC` y **todas las llaves**.

---

## ✅ Checklist del asesor

- [x] Repositorio con carpetas mínimas (`data/raw`, `notebooks`, `src/`).  
- [x] Dataset definido y disponible en `data/processed`.  
- [x] Scripts reproducibles: **ingesta** y **preprocesamiento** con **logs** y **hash**.  
- [x] EDA y **gráficos** en `reports/figures/`.  
- [x] Baseline mínimo: comparación de modelos por **PR-AUC**, umbral óptimo, **pipeline** y **metadatos** guardados.  
- [x] API lista para demo interna.

---

## 🗺️ Roadmap corto

1. Aumentar clase negativa (0) y enriquecer features de Empresa/Miembro.  
2. Calibración de probabilidades (isotonic) y explicabilidad (SHAP/permutación detallada).  
3. Orquestación (Makefile/DVC) y Docker para despliegue.  

---

## 👥 Créditos

Proyecto de tesis de maestría: **Detección de Riesgos de Corrupción en Obras Públicas**.  
Autores / contacto: _[agregar nombres y correo]_
