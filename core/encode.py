from __future__ import annotations
from typing import Dict, List, Tuple
import pandas as pd

def prepare_design_matrix(df: pd.DataFrame, predictors: List[str]) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """One-hot encode categoricals with drop-first; return X and baseline_levels mapping."""
    X = df[predictors].copy()
    baseline_levels: Dict[str, str] = {}
    # Coerce known categoricals to category dtype to control baseline if needed
    for col in predictors:
        if col in df.columns:
            s = df[col]
            if s.dtype == "object" or str(s.dtype).startswith("category"):
                X[col] = s.astype("category")
            elif col.lower() in {"sex", "educ", "period"}:
                X[col] = s.astype("category")
    # Determine baselines (first category after sorting)
    for col in predictors:
        if str(X[col].dtype).startswith("category"):
            cats = list(X[col].cat.categories)
            if len(cats) > 0:
                baseline_levels[col] = str(cats[0])
    X_enc = pd.get_dummies(X, drop_first=True)
    return X_enc, baseline_levels
