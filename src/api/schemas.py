from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BatchPredictRequest(BaseModel):
    """
    Estructura esperada para /predict_proba.
    'filas' es una lista de registros (dict) con columnas ~ al dataset de entrenamiento.
    """

    filas: List[Dict[str, Any]] = Field(..., min_length=1)

    # Permitimos claves variables (columnas) por fila, pero validamos vs meta.
    model_config = ConfigDict(extra="allow")

    @field_validator("filas")
    @classmethod
    def non_empty_rows(cls, v):
        for i, row in enumerate(v):
            if not isinstance(row, dict) or not row:
                raise ValueError(f"Fila {i} vacía o inválida.")
        return v


class PredictResponse(BaseModel):
    proba: float
    threshold: float
    riesgoso: bool


class PredictBatchResponse(BaseModel):
    resultados: List[PredictResponse]
