#!/usr/bin/python3
"""
    users views
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, make_response, request, jsonify


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def retreiveUsers():
    """ get list of users objects """
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def retreiveUserObj(user_id):
    """ retrieves a user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def createUser():
    """ create a user """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_instance = User(**request.get_json())
    new_instance.save()
    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteUser(user_id):
    """ deletes a user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}))


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def updateUser(user_id):
    """ update a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a Json"}), 400)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict())
