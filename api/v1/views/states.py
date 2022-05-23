#!/usr/bin/python3
"""
    states views
"""

import json
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, make_response, request, jsonify


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
def retreiveStates():
    """ get list of states objects """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def retreiveStateObj(state_id):
    """ retrieves a state by id """
    state = storage.get(State, state_id).to_dict()
    if state is None:
        abort(404)
    return jsonify(state)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def createState():
    """ create a state """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}, 400))
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_instance = State(**request.get_json())
    new_instance.save()
    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteState(state_id):
    """ deletes a state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}))


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def updateState(state_id):
    """ update a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a Json"}, 400))
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict())
