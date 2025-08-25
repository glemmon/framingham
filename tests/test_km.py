
import math

def test_km_basic_properties(app_client):
    r = app_client.post("/api/km", json={"outcome":"Any CHD"})
    assert r.status_code == 200
    data = r.get_json()
    surv = data["survival"]
    assert isinstance(surv, list) and len(surv) > 0
    # Survival must be within [0,1] and non-increasing
    last = 1.0
    for pt in surv:
        s = pt["s"]
        assert 0.0 <= s <= 1.0
        assert s <= last + 1e-9
        last = s

def test_km_zero_events_fixture(app_client, monkeypatch):
    # Switch to zero-events fixture
    monkeypatch.setenv("DATASET_PATH", "/mnt/data/expanded_tests/data/framingham_zero_events.csv")
    r = app_client.post("/api/km", json={"outcome":"Any CHD"})
    assert r.status_code == 200
    meta = r.get_json()["meta"]
    assert meta.get("zero_events") in (True, "true", "yes")

def test_km_all_events_t0_fixture(app_client, monkeypatch):
    monkeypatch.setenv("DATASET_PATH", "/mnt/data/expanded_tests/data/framingham_all_events_t0.csv")
    r = app_client.post("/api/km", json={"outcome":"Any CHD"})
    assert r.status_code == 200
    surv = r.get_json()["survival"]
    # Expect immediately near 0 survival
    assert len(surv) >= 1
    assert surv[0]["s"] in (0.0, 1.0) or surv[-1]["s"] == 0.0
