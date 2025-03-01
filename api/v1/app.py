#!/usr/bin/python3
"""
    API with FLASK
"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS


_host = getenv("HBNB_API_HOST", "0.0.0.0")
_port = getenv("HBNB_API_PORT", "5000")

app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def invalidRoute(e):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host=_host, port=_port, threaded=True)
