#!/usr/bin/python3
"""
    amenities views
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, make_response, request, jsonify


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def retreiveAmenities():
    """ get list of amenities objects """
    amenities = []
    for amenity in storage.all("amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def retreiveAmenityObj(amenity_id):
    """ retrieves a amenity by id """
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def createAmenity():
    """ create a amenity """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_instance = Amenity(**request.get_json())
    new_instance.save()
    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """ deletes a amenity by id """
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete(amenity)
    storage.save()
    return (jsonify({}))


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """ update a amenity """
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a Json"}), 400)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict())
