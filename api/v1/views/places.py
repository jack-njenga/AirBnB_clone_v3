#!/usr/bin/python3
"""
Handles all default RESTFul API actions:
    Retrieves the list of all Place objects of a City if
    (GET /api/v1/cities/<city_id>/places)
    Retrieves a Place object (GET /api/v1/places/<place_id>):
    Deletes a Place object (DELETE /api/v1/places/<place_id>)
    Creates a new Place in a City (POST /api/v1/cities/<city_id>/places)
    Updates a Place object (PUT /api/v1/places/<place_id>)
"""

from api.v1.views import app_views
from flask import jsonify, Flask, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"], strict_slashes=False)
def get_post_place(city_id):
    """
    Retrieves the list of all Place objects in a City if (GET)
    Creates new Place in City if (POST)
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        place_lst = []
        for place in city.places:
            place_lst.append(place.to_dict())
        return jsonify(place_lst)

    if request.method == "POST":
        data = request.get_json(silent=True)
        if data:
            if "name" not in data.keys():
                abort(400, "Missing name")
            if "user_id" not in data.keys():
                abort(400, "Missing user_id")
            curr_usr = storage.get(User, data["user_id"])
            if curr_usr:
                data["city_id"] = city_id
                new_plc = Place(**data)
                new_plc.save()
                return make_response(jsonify(new_plc.to_dict()), 201)
            else:
                abort(404)
        else:
            abort(400, "Not a JSON")


@app_views.route("/places/<place_id>>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_del_put_place(place_id):
    """
    Retrieves a Amenity object if (GET)
    Deletes a Amenity object if (DELETE)
    Updates a Amenity object if (PUT)
    """
    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())

    if request.method == "DELETE":
        if place.review:
            for review in places.reviews:
                storage.delete(review)
            storage.delete(place)
            storage.save()
        return make_response(jsonify({}), 200)

    if request.method == "PUT":
        check_list = ["id", "created_at", "updated_at", "user_id", "city_id"]
        data = request.get_json(silent=True)
        if data:
            for key, val in data.items():
                if key not in check_list:
                    setattr(place, key, val)
            place.save()
            return make_response(jsonify(place.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
