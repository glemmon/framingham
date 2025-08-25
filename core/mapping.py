from __future__ import annotations
from typing import Dict

# UI Outcome names -> event/time columns
DEFAULT_OUTCOME_MAP: Dict[str, Dict[str, str]] = {
    "Angina": {"event": "ANGINA", "time": "TIMEAP"},
    "Hospitalized MI": {"event": "HOSPMI", "time": "TIMEMI"},
    "MI or Fatal CHD": {"event": "MI_FCHD", "time": "TIMEMIFC"},
    "Any CHD": {"event": "ANYCHD", "time": "TIMECHD"},
    "Stroke": {"event": "STROKE", "time": "TIMESTRK"},
    "Any CVD": {"event": "CVD", "time": "TIMECVD"},
    "All-cause mortality": {"event": "DEATH", "time": "TIMEDTH"},
    "Incident Hypertension": {"event": "HYPERTEN", "time": "TIMEHYP"},
}

# Map event column back to a default UI outcome name (best effort)
EVENT_TO_OUTCOME = {v["event"]: k for k, v in DEFAULT_OUTCOME_MAP.items()}

# Map outcome to relevant prevalent exclusion flag
PREVALENT_BY_OUTCOME: Dict[str, str] = {
    "Any CHD": "PREVCHD",
    "MI or Fatal CHD": "PREVCHD",
    "Hospitalized MI": "PREVMI",
    "Angina": "PREVAP",
    "Stroke": "PREVSTRK",
    "Incident Hypertension": "PREVHYP",
    # For Any CVD and All-cause mortality, no direct prevalent exclusion flag; leave None
}

def outcome_key_for_event(event_col: str) -> str:
    return EVENT_TO_OUTCOME.get(event_col, event_col)
