#!/usr/bin/python3
"""
import app_views from api.v1.views, create status ok
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def api_status():
    """
    Returns a JSON response
    """
    response = {"status": "OK"}
    return jsonify(response)
