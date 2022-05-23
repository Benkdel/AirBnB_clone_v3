#!/usr/bin/python3
"""
    places views
"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, make_response, request, jsonify


@app_views.route("/states/<string:city_id>/places", methods=["GET"],
                 strict_slashes=False)
def retreivePlaces(city_id):
    """ get list of places from place object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<string:place_id>", methods=["GET"],
                 strict_slashes=False)
def retreivePlace(place_id):
    """ get place by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/cities/<string:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def createPlace(city_id):
    """ create a place """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    user = storage.get(User, request.get_json().get("user_id"))
    if user is None:
        abort(404)
    dict = request.get_json()
    dict["city_id"] = city_id
    new_instance = Place(**dict)
    new_instance.save()
    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def deletePlace(place_id):
    """ deletes a place by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                 strict_slashes=False)
def updatePlace(place_id):
    """ update a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a Json"}), 400)
    for key, val in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
