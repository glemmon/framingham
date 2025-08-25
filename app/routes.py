from __future__ import annotations
from flask import Blueprint, current_app, jsonify, request, send_file, render_template
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple

from core.mapping import DEFAULT_OUTCOME_MAP, outcome_key_for_event
from core.validate import infer_column_types, ValidationError, validate_event_time
from core.filters import apply_filters_and_remediations
from core.km import compute_km
from core.cox import fit_cox
from core.plotting import plot_km, plot_cox_forest

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/health")
def health():
    ok = hasattr(current_app, "registry") and current_app.registry is not None  # type: ignore[attr-defined]
    return jsonify({"status": "ok" if ok else "error", "dataset_loaded": ok})

@bp.route("/api/columns", methods=["GET"])
def api_columns():
    df = current_app.registry.df  # type: ignore[attr-defined]
    types = infer_column_types(df)
    defaults = DEFAULT_OUTCOME_MAP
    return jsonify({
        "columns": list(df.columns),
        "types": types,
        "defaults": defaults
    })

def _resolve_event_time(payload: Dict[str, Any]) -> Tuple[str, str, str]:
    outcome = payload.get("outcome")
    event_col = payload.get("event_col")
    time_col = payload.get("time_col")
    if outcome and not (event_col and time_col):
        mapping = DEFAULT_OUTCOME_MAP.get(outcome)
        if not mapping:
            raise ValidationError(f"Unknown outcome '{outcome}'.")
        event_col = mapping["event"]
        time_col = mapping["time"]
    if not (event_col and time_col):
        raise ValidationError("Must provide either an outcome or both event_col and time_col.")
    return outcome or outcome_key_for_event(event_col), event_col, time_col

@bp.route("/api/km", methods=["POST"])
def api_km():
    df = current_app.registry.df  # type: ignore[attr-defined]
    payload = request.get_json(force=True) or {}
    try:
        outcome_key, event_col, time_col = _resolve_event_time(payload)
        filters = payload.get("filters", {}) or {}
        validate_event_time(df, event_col, time_col)
        df_filt, meta, warnings = apply_filters_and_remediations(df, outcome_key, event_col, time_col, filters)
        km = compute_km(df_filt, event_col, time_col)
        km["meta"].update(meta)
        if warnings:
            km["meta"]["warnings"] = warnings
        return jsonify(km)
    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "KM computation failed", "detail": str(e)}), 500

@bp.route("/api/cox", methods=["POST"])
def api_cox():
    df = current_app.registry.df  # type: ignore[attr-defined]
    payload = request.get_json(force=True) or {}
    try:
        outcome_key, event_col, time_col = _resolve_event_time(payload)
        predictors = payload.get("predictors") or []
        if not predictors:
            raise ValidationError("At least one predictor is required for Cox PH.")
        missing = payload.get("missing", "drop")
        filters = payload.get("filters", {}) or {}
        validate_event_time(df, event_col, time_col)
        df_filt, meta, warnings = apply_filters_and_remediations(df, outcome_key, event_col, time_col, filters)
        res = fit_cox(df_filt, event_col, time_col, predictors, missing=missing)
        res["meta"].update(meta)
        if warnings:
            res["warnings"] = warnings
        return jsonify(res)
    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Cox computation failed", "detail": str(e)}), 500

@bp.route("/api/export_plot", methods=["POST"])
def api_export_plot():
    df = current_app.registry.df  # type: ignore[attr-defined]
    payload = request.get_json(force=True) or {}
    try:
        plot_type = payload.get("type")
        fmt = payload.get("format", "png")
        outcome_key, event_col, time_col = _resolve_event_time(payload)
        filters = payload.get("filters", {}) or {}
        validate_event_time(df, event_col, time_col)
        df_filt, meta, warnings = apply_filters_and_remediations(df, outcome_key, event_col, time_col, filters)
        buf = BytesIO()
        if plot_type == "km":
            km = compute_km(df_filt, event_col, time_col)
            fig = plot_km(km, title=f"{outcome_key} — Kaplan–Meier")
        elif plot_type == "cox":
            predictors = payload.get("predictors") or []
            if not predictors:
                raise ValidationError("Predictors required for Cox forest plot.")
            res = fit_cox(df_filt, event_col, time_col, predictors, missing=payload.get("missing","drop"))
            fig = plot_cox_forest(res, title=f"{outcome_key} — Cox PH (HR with 95% CI)")
        else:
            raise ValidationError("Unknown plot type. Use 'km' or 'cox'.")
        if fmt == "svg":
            fig.savefig(buf, format="svg", dpi=current_app.config["EXPORT_DPI"])
            mimetype = "image/svg+xml"
        else:
            fig.savefig(buf, format="png", dpi=current_app.config["EXPORT_DPI"])
            mimetype = "image/png"
        buf.seek(0)
        return send_file(buf, mimetype=mimetype, as_attachment=True, download_name=f"plot.{fmt}")
    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Plot export failed", "detail": str(e)}), 500
