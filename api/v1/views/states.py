#!/usr/bin/python3
"""
    states views
"""

import json
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, make_response, request


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
def retreiveStates():
    """ get list of states objects """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return json.dumps(states, indent=4)


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def retreiveStateObj(state_id):
    """ retrieves a state by id """
    state = storage.get(State, state_id).to_dict()
    if state is None:
        abort(404)
    return json.dumps(state, indent=4)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def createState():
    """ create a state """
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a JSON"},
                                        indent=4), 400)
    if "name" not in request.get_json():
        return make_response(json.dumps({"error": "Missing name"},
                                        indent=4), 400)
    new_instance = State(**request.get_json())
    new_instance.save()
    return make_response(json.dumps(new_instance.to_dict(),
                                    indent=4), 201)


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteState(state_id):
    """ deletes a state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (json.dumps({}, indent=4))


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def updateState(state_id):
    """ update a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a Json"},
                                        indent=4), 400)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    state.save()
    return json.dumps(state.to_dict(), indent=4)
