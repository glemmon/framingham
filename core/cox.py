from __future__ import annotations
from typing import Any, Dict, List
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import ConvergenceError

from .encode import prepare_design_matrix

def fit_cox(df: pd.DataFrame, event_col: str, time_col: str, predictors: List[str], missing: str = "drop") -> Dict[str, Any]:
    data = df[[time_col, event_col] + predictors].copy()
    if missing == "drop":
        data = data.dropna()
    else:
        # simple impute: numeric -> mean, categorical -> mode
        for col in data.columns:
            if col in (time_col, event_col):
                continue
            if pd.api.types.is_numeric_dtype(data[col]):
                data[col] = data[col].fillna(data[col].mean())
            else:
                data[col] = data[col].fillna(data[col].mode().iloc[0] if not data[col].mode().empty else data[col])
    X_enc, baseline_levels = prepare_design_matrix(data, predictors)
    # Combine with duration/event
    model_df = pd.concat([data[[time_col, event_col]].reset_index(drop=True), X_enc.reset_index(drop=True)], axis=1)
    cph = CoxPHFitter()
    converged = True
    warnings: List[str] = []
    try:
        cph.fit(model_df, duration_col=time_col, event_col=event_col, robust=True)
    except ConvergenceError as ce:
        converged = False
        warnings.append(str(ce))
    except Exception as e:
        converged = False
        warnings.append(str(e))
    rows: List[Dict[str, Any]] = []
    n = int(len(model_df))
    events = int(model_df[event_col].sum())
    censored = int((model_df[event_col] == 0).sum())
    if converged:
        summ = cph.summary
        # summary index are encoded columns; map back best-effort
        for enc_name, row in summ.iterrows():
            hr = float(np.exp(row["coef"]))
            lcl = float(np.exp(row["coef lower 95%"]))
            ucl = float(np.exp(row["coef upper 95%"]))
            p = float(row["p"])
            # Split enc_name into var and level if from dummy
            if "_" in enc_name and any(enc_name.startswith(p + "_") for p in predictors):
                var = enc_name.split("_")[0]
                level = enc_name[len(var)+1:]
            else:
                var = enc_name
                level = None
            rows.append({"var": var, "level": level, "hr": hr, "lcl": lcl, "ucl": ucl, "p": p})
    meta: Dict[str, Any] = {
        "baseline_levels": baseline_levels,
        "n": n,
        "events": events,
        "censored": censored,
        "encoding": "one_hot_drop_first",
        "missing": missing,
        "tie_method": "efron",
        "converged": converged,
    }
    return {"rows": rows, "meta": meta, "warnings": warnings}
