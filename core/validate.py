from __future__ import annotations
from typing import Dict
import pandas as pd
import numpy as np

class ValidationError(Exception):
    pass

def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
    types: Dict[str, str] = {}
    for c in df.columns:
        s = df[c]
        if pd.api.types.is_numeric_dtype(s):
            uniques = pd.unique(s.dropna())
            if set(np.unique(uniques)).issubset({0, 1}) and len(uniques) <= 2:
                types[c] = "binary"
            elif c.lower() in {"sex", "educ", "period"}:
                types[c] = "categorical"
            else:
                types[c] = "numeric"
        else:
            types[c] = "categorical"
    return types

def validate_event_time(df: pd.DataFrame, event_col: str, time_col: str) -> None:
    for col in [event_col, time_col]:
        if col not in df.columns:
            raise ValidationError(f"Column '{col}' not found in dataset.")
    ev = df[event_col]
    ti = df[time_col]
    # Event must be binary (0/1)
    vals = set(pd.unique(ev.dropna()))
    if not vals.issubset({0, 1}):
        raise ValidationError(f"Event column '{event_col}' must be binary (0/1).")
    # Time must be numeric and >= 0
    if not pd.api.types.is_numeric_dtype(ti):
        raise ValidationError(f"Time column '{time_col}' must be numeric (days).")
    if (ti < 0).any():
        raise ValidationError(f"Time column '{time_col}' contains negative values.")
