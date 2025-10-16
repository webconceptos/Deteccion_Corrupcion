# 🏗️ Sistema de Detección de Riesgos de Corrupción en Obras Públicas mediante Machine Learning

**Repositorio Oficial – Tesis de Maestría UNI (2025)**  
**Autor:** Fernando García - Hilario Aradiel
**Proyecto:** *“Sistema de Identificación de Obras Públicas con Riesgo de Corrupción en el Perú”*  
**Versión:** 1.0.0  
**Última actualización:** Octubre 2025  

---

## 🎯 Objetivo del Proyecto

Desarrollar un **Sistema Inteligente** que, a través de **Machine Learning**, permita **identificar Obras Públicas con riesgo potencial de corrupción** en el Perú, integrando datos de obras, empresas y funcionarios públicos.

El sistema aplica técnicas de **Análisis Exploratorio**, **Ingeniería de Características**, **Modelado Predictivo** y **Evaluación de Riesgo**, con despliegue de un servicio API escalable en **FastAPI** y contenedorizado mediante **Docker**.

---

## 🧭 Metodología General

| Fase | Descripción | Entregable |
|------|--------------|------------|
| 1. Recolección y Diccionario de Datos | Integración de fuentes institucionales (OSCE, MEF, Contraloría, SEACE, etc.). | Diccionario de Datos ML + Diccionario de Sistemas Fuente |
| 2. Preprocesamiento y Normalización | Limpieza, codificación categórica, imputación y unificación de llaves (Obra, Empresa, Funcionario). | Dataset unificado `dataset_obras.parquet` |
| 3. Análisis Exploratorio (EDA) | Identificación de patrones, correlaciones y variables críticas de riesgo. | Gráficos en `reports/figures/` |
| 4. Entrenamiento y Evaluación | Modelos ML (RandomForest, XGBoost, LogisticRegression) con métricas AUC, PR-AUC y F1. | `models/pipeline.pkl` + `pipeline_meta.json` |
| 5. Implementación de API | Despliegue del modelo vía `FastAPI` y pruebas unitarias. | `src/api/main.py` |
| 6. Aseguramiento de Calidad | Integración continua (CI/CD), validación y despliegue contenedorizado. | Workflow GitHub Actions + Dockerfile |

---

## 🧱 Arquitectura del Sistema

```
+-------------------------------------------+
|        Detección de Riesgos de Corrupción |
+-------------------------------------------+
|           FASTAPI (servicio REST)         |
|    • /predict_proba   • /health           |
|    • /model_meta      • /explain*         |
+-------------------------------------------+
|      Pipeline ML (pickle + metadata)      |
|    • dataset procesado                    |
|    • columnas entrenadas                  |
|    • umbral de decisión (F1)              |
+-------------------------------------------+
|   Preprocesamiento & Feature Engineering  |
|    • obras + empresas + funcionarios      |
|    • codificación, escalado, limpieza     |
+-------------------------------------------+
|     Fuentes Institucionales Integradas    |
|  OSCE | MEF | SEACE | Contraloría | BID   |
+-------------------------------------------+
```

---

## 🗂️ Estructura del Repositorio

```
Deteccion_Corrupcion/
├── .github/workflows/ci.yml
├── src/
│   ├── api/
│   │   ├── main.py
│   │   ├── deps.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   └── health.py
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── test_api.py
│   └── test_meta.py
├── data/
├── models/
├── reports/figures/
├── notebooks/
├── requirements.txt
├── requirements-dev.txt
├── Makefile
├── Dockerfile.prod
├── docker-compose.prod.yml
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## 🚀 API FastAPI

| Método | Ruta | Descripción |
|---------|------|-------------|
| `GET` | `/health` | Verifica disponibilidad del servicio |
| `GET` | `/model_meta` | Devuelve metadatos del modelo entrenado |
| `POST` | `/predict_proba` | Retorna la probabilidad de riesgo de corrupción |

**Ejemplo de solicitud**
```bash
curl -X POST "http://127.0.0.1:8000/predict_proba" ^
     -H "Content-Type: application/json" ^
     -d "{"filas": [{"monto_total": 1200000, "departamento": "LIMA", "empresa": "XYZ SAC"}]}"
```

**Ejemplo de respuesta**
```json
{
  "resultados": [
    {
      "proba": 0.74,
      "threshold": 0.62,
      "riesgoso": true
    }
  ]
}
```

---

## 🧪 Pruebas Automáticas

- **PyTest** → pruebas unitarias.  
- **Ruff** → linting PEP-8.  
- **GitHub Actions** → CI/CD (lint + test + smoke).

---

## 🐳 Despliegue con Docker

```bash
docker compose -f docker-compose.prod.yml up --build
```
Servicio disponible en: `http://localhost:8000/docs`

---

## 📊 Métricas del Modelo

| Métrica | Valor |
|----------|-------|
| ROC-AUC | 0.83 |
| PR-AUC | 0.79 |
| Precisión | 0.74 |
| Recall | 0.68 |
| F1-Score | 0.70 |

---

## 🧭 Próximos Desarrollos

- [ ] Endpoint `/explain` con interpretabilidad SHAP.  
- [ ] Calibración de probabilidades.  
- [ ] Dashboard web en React.  
- [ ] Registro de modelos en MLflow.

---

## 🧾 Licencia

**MIT License**  
© 2025 Fernando García - Hilario Aradiel – Todos los derechos reservados.

---

> *“La detección temprana de patrones de riesgo permite fortalecer la transparencia y prevenir la corrupción desde el análisis de datos.”*
