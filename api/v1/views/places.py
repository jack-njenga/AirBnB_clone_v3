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
            if "user_id" not in data.keys():
                abort(400, description="Missing user_id")
            curr_usr = storage.get(User, data["user_id"])
            if curr_usr:
                if "name" not in data.keys():
                    abort(400, description="Missing name")
                data["city_id"] = city_id
                new_plc = Place(**data)
                new_plc.save()
                return jsonify(new_plc.to_dict()), 201
            else:
                abort(404)
        else:
            abort(400, description="Not a JSON")


@app_views.route("/places/<place_id>",
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
            storage.delete(place)
            storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        check_list = ["id", "created_at", "updated_at", "user_id", "city_id"]
        data = request.get_json(silent=True)
        if data:
            for key, val in data.items():
                if key not in check_list:
                    setattr(place, key, val)
            place.save()
            return jsonify(place.to_dict()), 200
        else:
            abort(400, description="Not a JSON")


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def post_place():
    """
    Retrieves all Place objects depending of the
    JSON in the body of the request.
    """
    places = storage.all(Place).values()
    place_list = []

    data = request.get_json(silent=True)
    if data:
        try:
            states = data["states"]
            cities = data["cities"]
            amenities = data["amenities"]
        except Exception as e:
            states = []
            cities = []
            amenities = []

        empty = False
        if all(len(val) == 0 for val in data.values()):
            empty = True
        if not bool(data) or empty is True:
            for place in places:
                place_list.append(place.to_dict())
                # return jsonify(place_list)

        if len(states) > 0:
            for state_id in states:
                for place in places:
                    city = storage.get(City, str(place.city_id))
                    if state_id == city.state_id:
                        if place.to_dict() not in place_list:
                            place_list.append(place.to_dict())

        if len(cities) > 0:
            for city_id in cities:
                for place in places:
                    if city_id == place.city_id:
                        if place.to_dict() not in place_list:
                            place_list.append(place.to_dict())

        if len(amenities) > 0:
            place_list = []
            for place in places:
                all_amenities = place.amenities
                for amenity in all_amenities:
                    for amenity_id in amenities:
                        if amenity_id == amenity.id:
                            place_list.append(place.to_dict())

        return jsonify(place_list)
    else:
        abort(400, description="Not a JSON")
