
import time
import pytest

@pytest.mark.bench
@pytest.mark.skipif(pytest.config.getoption("--skip-bench") if hasattr(pytest, "config") else False, reason="benchmarks skipped by flag")
def test_km_performance_benchmark(app_client):
    t0 = time.perf_counter()
    r = app_client.post("/api/km", json={"outcome":"Any CHD"})
    assert r.status_code == 200
    dur = (time.perf_counter() - t0) * 1000
    # soft threshold: 2000ms
    assert dur < 4000, f"KM too slow: {dur:.1f} ms"

@pytest.mark.bench
@pytest.mark.skipif(pytest.config.getoption("--skip-bench") if hasattr(pytest, "config") else False, reason="benchmarks skipped by flag")
def test_cox_performance_benchmark(app_client):
    t0 = time.perf_counter()
    r = app_client.post("/api/cox", json={"outcome":"Any CHD", "predictors":["AGE","SYSBP","SEX","educ"]})
    assert r.status_code == 200
    dur = (time.perf_counter() - t0) * 1000
    # soft threshold: 5000ms
    assert dur < 7000, f"Cox too slow: {dur:.1f} ms"

def test_invalid_predictor_error(app_client):
    r = app_client.post("/api/cox", json={"outcome":"Any CHD", "predictors":["THIS_COLUMN_DOES_NOT_EXIST"]})
    assert r.status_code in (400, 422)
