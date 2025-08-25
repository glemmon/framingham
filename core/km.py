from __future__ import annotations
from typing import Dict, Any
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter

def compute_km(df: pd.DataFrame, event_col: str, time_col: str) -> Dict[str, Any]:
    kmf = KaplanMeierFitter()
    T = df[time_col].astype(float)
    E = df[event_col].astype(int)
    if E.sum() == 0:
        notes = ["zero_events:true"]
    else:
        notes = ["zero_events:false"]
    kmf.fit(T, event_observed=E, label="KM")
    surv = kmf.survival_function_
    ci = kmf.confidence_interval_ if hasattr(kmf, "confidence_interval_") else None
    # Flatten to list of dicts
    out = []
    for idx, row in surv.itertuples():
        t = float(idx) if not isinstance(idx, (int, float)) else float(idx)
        s = float(row)
        if ci is not None and idx in ci.index:
            lcl = float(ci.loc[idx].iloc[0])
            ucl = float(ci.loc[idx].iloc[1])
        else:
            lcl = s
            ucl = s
        out.append({"t": t, "s": s, "lcl": lcl, "ucl": ucl})
    meta = {
        "event_col": event_col,
        "time_col": time_col,
        "n": int(len(df)),
        "events": int(E.sum()),
        "censored": int((E == 0).sum()),
        "tie_method": "N/A (KM)",
        "notes": notes,
    }
    return {"survival": out, "meta": meta}
