from functools import lru_cache
import json
import pickle
from pathlib import Path
from typing import Any, Dict, Tuple

MODELS_DIR = Path("models")
PIPELINE_PKL = MODELS_DIR / "pipeline.pkl"
PIPELINE_META = MODELS_DIR / "pipeline_meta.json"

class ModelNotFoundError(RuntimeError): ...
class MetaNotFoundError(RuntimeError): ...

@lru_cache(maxsize=1)
def get_model_and_meta() -> Tuple[Any, Dict]:
    if not PIPELINE_PKL.exists():
        raise ModelNotFoundError(f"No existe {PIPELINE_PKL}")
    if not PIPELINE_META.exists():
        raise MetaNotFoundError(f"No existe {PIPELINE_META}")
    with open(PIPELINE_PKL, "rb") as f:
        pipeline = pickle.load(f)
    with open(PIPELINE_META, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return pipeline, meta
