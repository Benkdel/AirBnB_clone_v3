#!/usr/bin/python3
"""
    city views
"""

import json
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, make_response, request


@app_views.route("/states/<string:state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def retreiveCities(state_id):
    """ get list of cities from state object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return json.dumps(cities, indent=4)


@app_views.route("/cities/<string:city_id>", methods=["GET"],
                 strict_slashes=False)
def retreiveCity(city_id):
    """ get city by id """
    city = storage.get(City, city_id).to_dict()
    if city is None:
        abort(404)
    return json.dumps(city, indent=4)


@app_views.route("/states/<string:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def createCity(state_id):
    """ create a city """
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a JSON"},
                                        indent=4), 400)
    if "name" not in request.get_json():
        return make_response(json.dumps({"error": "Missing name"},
                                        indent=4), 400)

    state = storage.get(State, state_id).to_dict()
    if state is None:
        abort(404)
    dict = request.get_json()
    dict["state_id"] = state_id
    new_instance = City(**dict)
    new_instance.save()
    return make_response(json.dumps(new_instance.to_dict(),
                                    indent=4), 201)


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteCity(city_id):
    """ deletes a city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return (json.dumps({}, indent=4))


@app_views.route("/cities/<string:city_id>", methods=["PUT"],
                 strict_slashes=False)
def updateCity(city_id):
    """ update a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a Json"},
                                        indent=4), 400)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return json.dumps(city.to_dict(), indent=4)
