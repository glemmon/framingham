from __future__ import annotations
from typing import Dict, Tuple, List
import pandas as pd

from .mapping import PREVALENT_BY_OUTCOME

def apply_filters_and_remediations(df: pd.DataFrame, outcome_key: str, event_col: str, time_col: str,
                                   filters: Dict) -> Tuple[pd.DataFrame, Dict, List[str]]:
    """Apply prevalent-disease exclusion, PERIOD filter, smoking remediation.
    Returns (df_filtered, meta, warnings).
    """
    meta = {"filters": {}}
    warnings: List[str] = []

    # Exclude prevalent disease
    if filters.get("exclude_prevalent"):
        prev_col = PREVALENT_BY_OUTCOME.get(outcome_key)
        if prev_col and prev_col in df.columns:
            before = len(df)
            df = df[df[prev_col] != 1]
            meta["filters"]["exclude_prevalent"] = {prev_col: 1, "removed": before - len(df)}

    # PERIOD filter
    period = filters.get("PERIOD")
    if period is not None:
        before = len(df)
        df = df[df["PERIOD"] == period]
        meta["filters"]["PERIOD"] = {"value": period, "removed": before - len(df)}

    # Smoking inconsistency remediation
    smoking_fix = filters.get("smoking_fix", "leave")  # leave | coerce | drop
    incons = (df.get("CURSMOKE") == 0) & (df.get("CIGPDAY") > 0) if "CURSMOKE" in df and "CIGPDAY" in df else None
    if incons is not None and incons.any():
        cnt = int(incons.sum())
        meta["filters"]["smoking_inconsistencies"] = {"count": cnt, "action": smoking_fix}
        if smoking_fix == "coerce":
            df.loc[incons, "CIGPDAY"] = 0
        elif smoking_fix == "drop":
            before = len(df)
            df = df[~incons]
            meta["filters"]["smoking_inconsistencies"]["removed"] = before - len(df)
        else:
            warnings.append(f"{cnt} smoking inconsistencies detected (CURSMOKE=0 with CIGPDAY>0).")

    # Warn if HDLC/LDLC used without period filter (handled in cox where predictors known)
    return df, meta, warnings
