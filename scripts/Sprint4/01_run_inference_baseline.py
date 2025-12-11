"""
01_run_inference_baseline.py
----------------------------
Script del Sprint 4 para evaluar el modelo BASELINE.

Flujo:
1. Carga un dataset de evaluación (CSV).
2. Separa X (features) e y (target).
3. Aplica un preprocesamiento simple (o tu pipeline real) vía utils_sprint4.
4. Carga el modelo baseline (serializado con joblib).
5. Ejecuta inferencia.
6. Calcula métricas de clasificación estándar.
7. Guarda:
   - Métricas en CSV
   - Predicciones en CSV
   - Log detallado en models/sprint4/logs/

Uso típico:

python scripts/Sprint4/01_run_inference_baseline.py ^
    --data data/processed/dataset_modelado.csv ^
    --target-column riesgo_corrupcion ^
    --model-path models/sprint4/modelos/baseline.pkl
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from utils_sprint4 import (
    load_dataset,
    load_sklearn_model,
    save_metrics_csv,
    setup_logger,
    preprocess_features,
)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray | None = None,
) -> Dict[str, Any]:
    """
    Calcula un conjunto estándar de métricas de clasificación.

    Si se proporciona y_proba (probabilidades de la clase positiva),
    también intenta calcular ROC-AUC.
    """
    metrics: Dict[str, Any] = {}

    metrics["accuracy"] = accuracy_score(y_true, y_pred)
    metrics["precision_macro"] = precision_score(
        y_true, y_pred, average="macro", zero_division=0
    )
    metrics["recall_macro"] = recall_score(
        y_true, y_pred, average="macro", zero_division=0
    )
    metrics["f1_macro"] = f1_score(
        y_true, y_pred, average="macro", zero_division=0
    )

    # Si y_proba está disponible y es binario, calculamos ROC-AUC
    if y_proba is not None:
        try:
            metrics["roc_auc"] = roc_auc_score(y_true, y_proba)
        except Exception:
            # Por si las clases, formato u otra cosa no permite ROC-AUC
            metrics["roc_auc"] = float("nan")

    return metrics


def main(args: argparse.Namespace) -> None:
    # ------------------------------------------------------------------
    # 1. Logger
    # ------------------------------------------------------------------
    logger = setup_logger(args.log_path)
    logger.info("=== Evaluación BASELINE - Sprint 4 ===")

    # ------------------------------------------------------------------
    # 2. Carga de dataset
    # ------------------------------------------------------------------
    data_path = Path(args.data)
    logger.info(f"Cargando dataset desde: {data_path}")
    df = load_dataset(data_path)

    if args.target_column not in df.columns:
        raise ValueError(
            f"La columna objetivo '{args.target_column}' no está en el dataset."
        )

    # Separar X, y
    y = df[args.target_column]
    X = df.drop(columns=[args.target_column])

    logger.info(f"Dataset cargado con shape: {df.shape}")
    logger.info(f"Número de features: {X.shape[1]}")

    # ------------------------------------------------------------------
    # 3. Preprocesamiento de features
    #    (usa la función genérica; puedes sustituir por tu pipeline real)
    # ------------------------------------------------------------------
    logger.info("Aplicando preprocesamiento de features (utils_sprint4.preprocess_features)…")
    X_proc = preprocess_features(X)

    # ------------------------------------------------------------------
    # 4. Carga de modelo baseline
    # ------------------------------------------------------------------
    model_path = Path(args.model_path)
    logger.info(f"Cargando modelo baseline desde: {model_path}")
    model = load_sklearn_model(model_path)

    # ------------------------------------------------------------------
    # 5. Inferencia
    # ------------------------------------------------------------------
    logger.info("Ejecutando inferencia con el modelo baseline…")
    y_pred = model.predict(X_proc)

    # Probabilidades (si el modelo lo soporta)
    y_proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(X_proc)
            # Si es binario, usamos proba de la clase positiva
            if proba.shape[1] == 2:
                y_proba = proba[:, 1]
        except Exception as e:
            logger.warning(f"No se pudo obtener predict_proba: {e}")

    # ------------------------------------------------------------------
    # 6. Cálculo de métricas
    # ------------------------------------------------------------------
    logger.info("Calculando métricas de desempeño…")
    metrics = compute_classification_metrics(
        y_true=y.values,
        y_pred=y_pred,
        y_proba=y_proba,
    )
    logger.info(f"Métricas baseline: {metrics}")

    # ------------------------------------------------------------------
    # 7. Guardado de métricas y predicciones
    # ------------------------------------------------------------------
    metrics_out = Path(args.metrics_out)
    preds_out = Path(args.predictions_out)

    logger.info(f"Guardando métricas en: {metrics_out}")
    save_metrics_csv(metrics, metrics_out)

    logger.info(f"Guardando predicciones en: {preds_out}")
    preds_df = pd.DataFrame(
        {
            "y_true": y.values,
            "y_pred": y_pred,
        }
    )
    if y_proba is not None:
        preds_df["y_proba"] = y_proba

    preds_out.parent.mkdir(parents=True, exist_ok=True)
    preds_df.to_csv(preds_out, index=False)

    logger.info("=== Evaluación baseline completada correctamente ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluación del modelo BASELINE (Sprint 4)."
    )
    parser.add_argument(
        "--data",
        required=True,
        help="Ruta al CSV de evaluación (ej. data/processed/dataset_modelado.csv).",
    )
    parser.add_argument(
        "--target-column",
        required=True,
        help="Nombre de la columna objetivo en el dataset.",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Ruta al modelo baseline serializado (ej. models/sprint4/modelos/baseline.pkl).",
    )
    parser.add_argument(
        "--metrics-out",
        default="models/sprint4/resultados/metrics_baseline.csv",
        help="Ruta de salida para las métricas.",
    )
    parser.add_argument(
        "--predictions-out",
        default="models/sprint4/resultados/predicciones_baseline.csv",
        help="Ruta de salida para las predicciones.",
    )
    parser.add_argument(
        "--log-path",
        default="models/sprint4/logs/inference_baseline.log",
        help="Ruta del archivo de log.",
    )

    main(parser.parse_args())

