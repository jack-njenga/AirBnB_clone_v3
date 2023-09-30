#!/usr/bin/python3
"""
Handles all default RESTFul API actions:
    Retrieves the list of all State objects (GET /api/v1/states)
    Retrieves a State object (GET /api/v1/states/<state_id>):
    Deletes a State object (DELETE /api/v1/states/<state_id>)
    Creates a State (POST /api/v1/states)
    Updates a State object (PUT /api/v1/states/<state_id>)
"""

from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET", "POST"], strict_slashes=False)
def get_all_post_states():
    """
    Retrieves the list of all State objects if (GET)
    Creates a State (POST)
    """
    if request.method == "GET":
        all_states = storage.all(State)
        st_lst = []
        for state in all_states.values():
            st_lst.append(state.to_dict())
        return jsonify(st_lst)

    if request.method == "POST":
        data = request.get_json(silent=True)
        if data:
            if data.get("name") is None:
                abort(400, "Missing name")
            else:
                new_state = State(**data)
                new_state.save()
                return jsonify(new_state.to_dict()), 201
        else:
            abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def del_state(state_id):
    """
    Retrieves a State object if (GET)
    Deletes a State object if (DELETE)
    Updates a State object if (PUT)
    """
    if request.method == "GET":
        state = storage.get(State, str(state_id))
        if state is None:
            abort(404)
        else:
            return jsonify(state.to_dict())

    if request.method == "DELETE":
        state = storage.get(State, str(state_id))
        if state is None:
            abort(404)
        else:
            # storage.delete(state)
            for city in state.cities:
                for place in city.places:
                    for review in place.reviews:
                        storage.delete(review)
                    storage.delete(place)
                storage.delete(city)
            storage.delete(state)
            storage.save()
            return jsonify({}), 200

    if request.method == "PUT":
        state = storage.get(State, str(state_id))
        if state is None:
            abort(404)
        else:
            data = request.get_json(silent=True)
            if data:
                for key, val in data.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(state, key, val)
                state.save()
                return jsonify(state.to_dict()), 200
            else:
                abort(400, "Not a JSON")
