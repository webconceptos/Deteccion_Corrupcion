# Informe Final Sprint 4

## Modelos Evaluados
|    | modelo       | best_params                                                                                       |        f1 |   roc_auc |
|---:|:-------------|:--------------------------------------------------------------------------------------------------|----------:|----------:|
|  0 | RandomForest | {'clf__max_depth': None, 'clf__min_samples_split': 2, 'clf__n_estimators': 200}                   | 0.241309  |  0.493026 |
|  1 | XGBoost      | {'clf__learning_rate': 0.1, 'clf__max_depth': 6, 'clf__n_estimators': 400, 'clf__subsample': 0.8} | 0.0982318 |  0.497479 |
|  2 | LogReg       | {'clf__C': 0.1, 'clf__penalty': 'l2', 'clf__solver': 'lbfgs'}                                     | 0         |  0.502987 |

## Slices Problemáticos
|    | slice_columna   | slice_valor                                     |   n |       f1 |   accuracy |   roc_auc |
|---:|:----------------|:------------------------------------------------|----:|---------:|-----------:|----------:|
|  0 | SECTOR          | DEFENSA Y SEGURIDAD NACIONAL                    |  50 | 0.571429 |   0.88     |  0.6675   |
|  1 | SECTOR          | PESCA                                           |  30 | 0.625    |   0.8      |  0.925466 |
|  2 | DEPARTAMENTO    | ICA                                             |  33 | 0.736842 |   0.848485 |  0.801653 |
|  3 | SECTOR          | JUSTICIA                                        |  49 | 0.774194 |   0.857143 |  0.852941 |
|  4 | ESTADO_OBRA     | EN EJECUCIÓN                                    | 133 | 0.78125  |   0.894737 |  0.927405 |
|  5 | DEPARTAMENTO    | AYACUCHO                                        |  89 | 0.782609 |   0.88764  |  0.874375 |
|  6 | DEPARTAMENTO    | LA LIBERTAD                                     |  53 | 0.8      |   0.90566  |  0.846154 |
|  7 | SECTOR          | PLANEAMIENTO; GESTIÓN Y RESERVA DE CONTINGENCIA | 123 | 0.8      |   0.926829 |  0.887986 |
|  8 | DEPARTAMENTO    | APURIMAC                                        |  33 | 0.8      |   0.909091 |  0.8575   |
|  9 | DEPARTAMENTO    | PIURA                                           | 140 | 0.810127 |   0.892857 |  0.921902 |

## Conclusiones
- El modelo con mejor F1 es seleccionado como final.
- Los slices permiten identificar segmentos de riesgo.
- SHAP aporta interpretabilidad técnica valiosa.
