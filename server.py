import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = b'abc-xyz'


def init_app():
    # return
    from internal.routers.routes import bp
    app.register_blueprint(bp, url_prefix="/api/v1")
    app.config["JSON_SORT_KEYS"] = False
    return app


if __name__ == '__main__':
    app = init_app()

    host = os.environ.get("HOST", "0.0.0.0")
    port = os.environ.get("PORT", 3001)
    debug = os.environ.get("DEBUG", False)
    app.run(host=host, port=port, debug=debug)
