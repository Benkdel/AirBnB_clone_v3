#!/usr/bin/python3
"""
    users views
"""

import json
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, make_response, request


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def retreiveUsers():
    """ get list of users objects """
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return json.dumps(users, indent=4)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def retreiveUserObj(user_id):
    """ retrieves a user by id """
    user = storage.get(User, user_id).to_dict()
    if user is None:
        abort(404)
    return json.dumps(user, indent=4)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def createUser():
    """ create a user """
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a JSON"},
                                        indent=4), 400)
    if "name" not in request.get_json():
        return make_response(json.dumps({"error": "Missing name"},
                                        indent=4), 400)
    new_instance = User(**request.get_json())
    new_instance.save()
    return make_response(json.dumps(new_instance.to_dict(),
                                    indent=4), 201)


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteUser(user_id):
    """ deletes a user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return (json.dumps({}, indent=4))


@app_views.route("/users/<string:user_id>", methods=["PUT"], strict_slashes=False)
def updateUser(user_id):
    """ update a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a Json"}, indent=4), 400)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return json.dumps(user.to_dict(), indent=4)
