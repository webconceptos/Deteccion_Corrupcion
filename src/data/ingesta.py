from pathlib import Path
from typing import Union

import pandas as pd


def leer_excel(path: Union[str, Path], sheet_name=0) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name)


def leer_csv(path: Union[str, Path], sep=",") -> pd.DataFrame:
    return pd.read_csv(path, sep=sep)


def guardar_parquet(df: pd.DataFrame, path: Union[str, Path]):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
