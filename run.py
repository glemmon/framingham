from app import create_app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")
    app = create_app()
    app.run(host=host, port=port, debug=os.environ.get("DEBUG", "0") == "1")
