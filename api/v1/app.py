#!/usr/bin/python3
"""
script that create flask app and registers blueprint app views to Flask ins
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

'''register the app_views bluprint to app '''
app.register_blueprint(app_views)

'''teardown function to close session '''


@app.teardown_appcontext
def teardown_session(exception):
    storage.close()


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
