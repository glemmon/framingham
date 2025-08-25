
def test_default_mapping_anychd(app_client):
    # Request KM without explicit columns -> should map Any CHD -> (ANYCHD, TIMECHD)
    payload = {"outcome": "Any CHD"}
    r = app_client.post("/api/km", json=payload)
    assert r.status_code == 200
    meta = r.get_json().get("meta", {})
    assert meta.get("event_col") in ("ANYCHD","anychd")
    assert meta.get("time_col") in ("TIMECHD","timechd")

def test_override_mapping(app_client):
    payload = {"outcome": "Any CHD", "event_col": "ANYCHD", "time_col": "TIMECHD"}
    r = app_client.post("/api/km", json=payload)
    assert r.status_code == 200
    meta = r.get_json()["meta"]
    assert meta["event_col"] == "ANYCHD"
    assert meta["time_col"] == "TIMECHD"
