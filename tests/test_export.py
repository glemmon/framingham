
def test_export_km_png(app_client):
    r = app_client.post("/api/export_plot", json={"type":"km","outcome":"Any CHD","format":"png"})
    assert r.status_code == 200
    assert r.content_type in ("image/png", "application/octet-stream")
    assert len(r.data) > 1000  # basic size sanity

def test_export_cox_svg(app_client):
    r = app_client.post("/api/export_plot", json={"type":"cox","outcome":"Any CHD","predictors":["AGE","SYSBP"],"format":"svg"})
    assert r.status_code == 200
    assert r.content_type in ("image/svg+xml", "image/svg")
    assert r.data.startswith(b"<?xml") or b"<svg" in r.data[:100].lower()
