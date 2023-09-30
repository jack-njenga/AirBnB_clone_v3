#!/usr/bin/python3
"""
script that create flask app and registers blueprint app views to Flask ins
"""

from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(exception):
    """
    Closes the session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    returns a JSON-formatted 404 status code response
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST"):
        host = os.getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if os.getenv("HBNB_API_PORT"):
        port = os.getenv("HBNB_API_PORT")
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True, debug=True)
