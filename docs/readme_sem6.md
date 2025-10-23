# Semana 6 – Modelado Predictivo y Comparativos (A/B)

**Objetivo:** entrenar variantes de modelos supervisados, comparar métricas y seleccionar el mejor para la siguiente fase.

## Modelos evaluados
- `logreg` → Regresión Logística (baseline)  
- `rf` → Random Forest (200 árboles)  
- `xgb` → XGBoost (profundidad 6, lr 0.1)  
- `mlp` (opcional) → Perceptrón Multicapa (64–32 neuronas)

## Métricas principales
| Modelo | F1 CV | ROC-AUC CV | PR-AUC CV |
|:-------|------:|-----------:|----------:|
| logreg | ≈ 0.67 | 0.74 | 0.70 |
| rf  | ≈ 0.75 | 0.82 | 0.78 |
| xgb  | **0.81** | **0.88** | **0.84** |
| mlp  | 0.77 | 0.86 | 0.80 |

> **Modelo seleccionado:** XGBoost  
> Mayor F1 y AUC con tiempo moderado y mejor capacidad explicativa (XAI – SHAP próxima semana).

## Artefactos generados
- `models/pipeline.pkl` – pipeline entrenado  
- `models/pipeline_meta.json` – metadatos (F1/AUC)  
- `reports/figures/sem6_pr_curve.png`, `sem6_roc_curve.png`

## Reproducibilidad
```bash
python scripts/train_models.py --folds 5
python scripts/eval_holdout.py --test-file data/processed/dataset_obras.parquet
python scripts/plot_curves.py --data data/processed/dataset_obras.parquet