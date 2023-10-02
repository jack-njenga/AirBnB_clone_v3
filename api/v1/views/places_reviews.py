#!/usr/bin/python3
"""
Handles all default RESTFul API actions:
    Retrieves the list of all review objects (GET /api/v1/places)
    Retrieves a review object (GET /api/v1/states/<state_id>):
    Deletes a review object (DELETE /api/v1/reviews/<review_id>)
    Creates a review (POST /api/v1/places/<place_id>/reviews)
    Updates a review object (PUT /api/v1/reviews/<review_id>)
"""


from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from api.v1.views import app_views
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getreview_from_places(place_id):
    """
    this searches for reviews by id
    """
    review_obj = storage.get(Place, place_id)
    if review_obj is None:
        abort(404)

    for review in review_obj:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    gets review id
    """
    review_obj = storage.get(Review, review_id)
    if review_id is None:
        abort(404)
    else:
        return jsonify(review_id.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """
    deletes review
    """
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    else:
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """
    creates a new place from state
    """
    '''create a variable for http header type'''
    header_type = request.headers.get('Content-Type')
    if (header_type == 'application/json'):
        # if not json, returns a dict or list
        # else, return error for 404 or 400
        if place is None:
            abort(404)
        data = request.get_json()
        if 'user_id' not in data:
            abort(400, 'Missing text')
        user_obj = storage.get(User, data["user_id"])
        if user_obj is None:
            abort(404)
        if 'text' not in data:
            abort(400, 'Missing text')
        '''returns new review with status 201'''
        new_review = Review(**data)
        setattr(new_review, 'place_id', place_id)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    else:
        abort(400, 'Not a JSON')


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """
    updates review
    """
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(object, key, value)
    storage.save()
    return jsonify(object.to_dict()), 200
