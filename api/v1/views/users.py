#!/usr/bin/python3
"""
Handles all default RESTFul API actions:
    Retrieves the list of all User objects if
    (GET /api/v1/users)
    Retrieves a User object (GET /api/v1/users/<user_id>):
    Deletes a User object (DELETE /api/v1/users/<user_id>)
    Creates a User (POST /api/v1/users)
    Updates a User object (PUT /api/v1/users/<user_id>)
"""

from api.v1.views import app_views
from flask import jsonify, Flask, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def get_post_user():
    """
    Retrieves the list of all User objects if (GET)
    Creates new User if (POST)
    """
    users = storage.all(User)
    if users is None:
        abort(404)
    if request.method == "GET":
        user_lst = []
        for user in users.values():
            user_lst.append(user.to_dict())
        return jsonify(user_lst)

    if request.method == "POST":
        data = request.get_json(silent=True)
        if data:
            if "email" not in data.keys():
                abort(400, description="Missing email")
            if "password" not in data.keys():
                abort(400, description="Missing password")
            new_usr = User(**data)
            new_usr.save()
            return jsonify(new_usr.to_dict()), 201
        else:
            abort(400, description="Not a JSON")


@app_views.route("/users/<user_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_del_put_user(user_id):
    """
    Retrieves a User object if (GET)
    Deletes a User object if (DELETE)
    Updates a User object if (PUT)
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())

    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        check_list = ["id", "created_at", "updated_at", "email"]
        data = request.get_json(silent=True)
        if data:
            for key, val in data.items():
                if key not in check_list:
                    setattr(user, key, val)
            user.save()
            return jsonify(user.to_dict()), 200
        else:
            abort(400, description="Not a JSON")
