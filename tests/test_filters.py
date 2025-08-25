
def test_exclude_prevalent_for_chd(app_client):
    payload = {"outcome":"Any CHD", "predictors":["AGE","SYSBP"], "filters":{"exclude_prevalent": True}}
    r = app_client.post("/api/cox", json=payload)
    assert r.status_code == 200
    meta = r.get_json().get("meta", {})
    excluded = meta.get("excluded", {})
    # Accept different encodings but require that CHD prevalent exclusion is indicated
    assert "PREVCHD" in str(excluded) or "prevchd" in str(excluded)
