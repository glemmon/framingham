
def test_homepage(app_client):
    r = app_client.get("/")
    assert r.status_code == 200
    assert b"<html" in r.data.lower()

def test_health(app_client):
    r = app_client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data.get("status") == "ok"
