
import pytest

def test_cox_single_predictor(app_client):
    payload = {"outcome":"Any CHD", "predictors":["AGE"]}
    r = app_client.post("/api/cox", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert "rows" in data and isinstance(data["rows"], list)
    assert any(row["var"] == "AGE" for row in data["rows"])

def test_cox_multiple_predictors(app_client):
    payload = {"outcome":"Any CHD", "predictors":["AGE","SYSBP","SEX","educ"]}
    r = app_client.post("/api/cox", json=payload)
    assert r.status_code == 200
    rows = r.get_json()["rows"]
    vars_present = set(r["var"] for r in rows)
    for v in ["AGE","SYSBP"]:
        assert v in vars_present

def test_cox_categorical_encoding_baseline(app_client):
    payload = {"outcome":"Any CHD", "predictors":["SEX","educ"]}
    r = app_client.post("/api/cox", json=payload)
    assert r.status_code == 200
    meta = r.get_json().get("meta", {})
    assert "baseline_levels" in meta

def test_cox_collinearity_detected(app_client, monkeypatch):
    monkeypatch.setenv("DATASET_PATH", "/mnt/data/expanded_tests/data/framingham_collinear.csv")
    payload = {"outcome":"Any CHD", "predictors":["SYSBP","SYSBP_dup"]}
    r = app_client.post("/api/cox", json=payload)
    # Either explicit error or warning in meta
    data = r.get_json()
    assert r.status_code in (200, 422, 400)
    assert ("error" in data) or ("warnings" in data) or ("collinearity" in str(data).lower())

def test_cox_missingness_handling_drop(app_client, monkeypatch):
    monkeypatch.setenv("DATASET_PATH", "/mnt/data/expanded_tests/data/framingham_missing_predictors.csv")
    payload = {"outcome":"Any CHD", "predictors":["AGE","SYSBP"], "missing":"drop"}
    r = app_client.post("/api/cox", json=payload)
    assert r.status_code == 200
    meta = r.get_json().get("meta", {})
    assert meta.get("missing") in ("drop", "impute")

def test_cox_period3_lipids_warning(app_client):
    payload = {"outcome":"Any CHD", "predictors":["HDLC","LDLC","AGE"]}
    r = app_client.post("/api/cox", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    warn = "warnings" in data and any("PERIOD=3" in w for w in data["warnings"])
    # allow either auto-filter or warning
    ok = warn or ("meta" in data and data["meta"].get("filters", {}).get("PERIOD") == 3)
    assert ok
