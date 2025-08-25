
import os
import importlib
import json
import pytest

from flask import Flask

APP_IMPORT_PATH = os.environ.get("APP_IMPORT_PATH", "app")
FACTORY = os.environ.get("APP_FACTORY", "create_app")
DATASET_PATH = os.environ.get("DATASET_PATH", "/mnt/data/Framingham.csv")

@pytest.fixture(scope="session")
def app() -> Flask:
    mod = importlib.import_module(APP_IMPORT_PATH)
    factory = getattr(mod, FACTORY)
    # Allow tests to override dataset path:
    app = factory({"DATASET_PATH": DATASET_PATH})
    return app

@pytest.fixture()
def app_client(app):
    return app.test_client()

def pytest_addoption(parser):
    parser.addoption("--skip-bench", action="store_true", default=False, help="skip benchmark tests")

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with -m 'not slow')")
    config.addinivalue_line("markers", "bench: marks benchmark tests")

