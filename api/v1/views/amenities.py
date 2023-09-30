#!/usr/bin/python3
"""
Handles all default RESTFul API actions:
    Retrieves the list of all Amenity objects if
    (GET /api/v1/amenities/<amenity_id>)
    Retrieves a Amenity object (GET /api/v1/amenities/<amenity_id>):
    Deletes a Amenity object (DELETE /api/v1/amenities/<amenity_id>)
    Creates a Amenity (POST /api/v1/amenities)
    Updates a Amenity object (PUT /api/v1/amenities/<amenity_id>)
"""

from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"],
                 strict_slashes=False)
def get_post_Amenity():
    """
    Retrieves the list of all Amenity objects if (GET)
    Creates new Amenity if (POST)
    """
    amenities = storage.all(Amenity)
    if amenities is None:
        abort(404)
    if request.method == "GET":
        amenity_lst = []
        for amenity in amenities.values():
            amenity_lst.append(amenity.to_dict())
        return jsonify(amenity_lst), 200

    if request.method == "POST":
        data = request.get_json()
        if data:
            if "name" not in data.keys():
                abort(400, "Missing name")
            else:
                new_amt = Amenity(**data)
                new_amt.save()
                return jsonify(new_amt.to_dict()), 201
        else:
            abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_del_put_amenity(amenity_id):
    """
    Retrieves a Amenity object if (GET)
    Deletes a Amenity object if (DELETE)
    Updates a Amenity object if (PUT)
    """
    amenity = storage.get(Amenity, str(amenity_id))
    if amenity is None:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict()), 200

    if request.method == "DELETE":
        if amenity:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200

    if request.method == "PUT":
        check_list = ["id", "created_at", "updated_at"]
        if amenity:
            data = request.get_json()
            if data:
                for key, val in data.items():
                    if key not in check_list:
                        setattr(amenity, key, val)
                amenity.save()
                return jsonify(amenity.to_dict()), 200
            else:
                abort(400, "Not a JSON")
