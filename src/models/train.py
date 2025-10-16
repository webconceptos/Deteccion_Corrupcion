import argparse
from pathlib import Path

import joblib
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


def get_model(kind: str):
    if kind == "rf":
        return RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
    if kind == "xgb":
        return XGBClassifier(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            n_jobs=-1,
            random_state=42,
        )
    if kind == "lgbm":
        return LGBMClassifier(
            n_estimators=400, learning_rate=0.05, max_depth=-1, random_state=42, n_jobs=-1
        )
    raise ValueError(f"Modelo no soportado: {kind}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Ruta al dataset (csv/parquet)")
    p.add_argument("--target", required=True, help="Nombre de la columna objetivo")
    p.add_argument("--model", default="rf", choices=["rf", "xgb", "lgbm"])
    p.add_argument("--out", default="models/model.pkl")
    args = p.parse_args()

    # Carga
    if args.input.endswith(".parquet"):
        df = pd.read_parquet(args.input)
    else:
        df = pd.read_csv(args.input)

    y = df[args.target].astype(int)
    X = df.drop(columns=[args.target])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = get_model(args.model)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, digits=4))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.out)
    print(f"Modelo guardado en: {args.out}")


if __name__ == "__main__":
    main()
