#!/usr/bin/python3
"""
imports app_views from api.vi.views and creates a route
"/status" on obj "app_views" that returns a JSON "status": "OK"
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    ''' returns a JSON'''

    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def stats():
    '''endpoint that retrieves the number of each objects by type'''
    stats = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
     }
    return jsonify(stats)
