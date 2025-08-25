from flask import Flask
from .routes import bp as routes_bp
from .settings import Settings
from core.dataset import DataRegistry

import os

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Settings())
    app.config['EXPLAIN_TEMPLATE_LOADING'] = True
    # Load dataset at startup
    registry = DataRegistry(app.config["DATASET_PATH"])
    app.registry = registry  # type: ignore[attr-defined]
    app.register_blueprint(routes_bp)
    return app
