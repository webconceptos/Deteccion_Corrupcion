from fastapi import APIRouter

from src.api.deps import get_model_and_meta

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    try:
        _ = get_model_and_meta()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@router.get("/model_meta")
def model_meta():
    _, meta = get_model_and_meta()
    # Filtra campos largos si fuese necesario
    safe = {k: v for k, v in meta.items() if k not in {"feature_importances_raw"}}
    return safe
