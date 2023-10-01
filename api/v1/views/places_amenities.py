#!/usr/bin/python3
"""
Creates a new view for the link between Place objects and
Amenity objects that handles all default RESTFul API actions
"""

from flas import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenities import Amenity
d_b = os.getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"], strict_slashes=False)
def get_amenity(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404)

    amenity_list = []
    if d_b == "db":
        for amenity in place.amenities:
            amenity_list.append(amenity.to_dict())
    else:
        for amty_id in place.amenity_ids:
            amty = storage.get(Amenity, amty_id)
            amenity_list.append(amty)
    return jsonify(amenity_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"], strict_slashes=False)
def del_post_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    """
    place = storage.get(Place, str(place_id))
    amenity = storage.get(Amenity, str(amenity_id))
    if place is None or amenity is None:
        abort(404)

    if request.method == "DELETE":
        if d_b = "db":
            if amenity in place.amenities:
                place.amenities.remove(amenity)
            else:
                abort(404)
        else:
            if amenity_id in place.amenity_ids:
                place.amenity_ids.remove(amenity_id)
            else:
                abort(404)
        place.save()
        storage.save()
        return jsonify({}), 200

    if request.method == "POST":
        if d_b == "db":
            if amenities in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenity_ids.append(str(amenity_id))
        place.save()
        storage.save()
        return jsonify(amenity.to_dict()), 201
