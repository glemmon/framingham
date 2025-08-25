
import os
import pytest

def test_columns_endpoint(app_client):
    r = app_client.get("/api/columns")
    assert r.status_code == 200
    data = r.get_json()
    assert "columns" in data and isinstance(data["columns"], list)
    assert "types" in data and isinstance(data["types"], dict)
    assert "defaults" in data and isinstance(data["defaults"], dict)

@pytest.mark.xfail(reason="App needs to expose a way to simulate missing dataset", strict=False)
def test_missing_dataset_error(monkeypatch, app_client):
    # This is a placeholder; flip to real when app allows config reload
    r = app_client.get("/api/columns")
    assert r.status_code == 503
