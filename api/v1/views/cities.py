#!/usr/bin/python3
"""
Handles all default RESTFul API actions:
    Retrieves the list of all City objects (GET /api/v1/states)
    Retrieves a City object (GET /api/v1/states/<state_id>):
    Deletes a City object (DELETE /api/v1/states/<state_id>)
    Creates a City (POST /api/v1/states)
    Updates a City object (PUT /api/v1/states/<state_id>)
"""

from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def get_post_city(state_id):
    """
    Retrieves the list of all City  objects of a State if (GET)
    Creates a State (POST)
    """
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    if request.method == "GET":
        city_lst = []
        for city in state.cities:
            city_lst.append(city.to_dict())
        return jsonify(city_lst)

    if request.method == "POST":
        data = request.get_json(silent=True)
        if data:
            if "name" not in data.keys():
                abort(400, "Missing name")
            else:
                data["state_id"] = state_id
                new_city = City(**data)
                new_city.save()
                return jsonify(new_city.to_dict()), 201
        else:
            abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_del_put_city(city_id):
    """
    Retrieves a City object if (GET)
    Deletes a City object if (DELETE)
    Updates a City object if (PUT)
    """
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())

    if request.method == "DELETE":
        if city:
            for place in city.places:
                for review in place.reviews:
                    storage.delete(review)
                storage.delete(place)
            storage.delete(city)
            storage.save()
            return jsonify({}), 200

    if request.method == "PUT":
        check_list = ["id", "created_at", "updated_at", "state_id"]
        if city:
            data = request.get_json()
            if data:
                for key, val in data.items():
                    if key not in check_list:
                        setattr(city, key, val)
                city.save()
                return jsonify(city.to_dict()), 200
            else:
                abort(400, "Not a JSON")
