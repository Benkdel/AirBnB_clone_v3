#!/usr/bin/python3
"""
    amenities views
"""

import json
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, make_response, request


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def retreiveAmenities():
    """ get list of amenities objects """
    amenities = []
    for amenity in storage.all("amenity").values():
        amenities.append(amenity.to_dict())
    return json.dumps(amenities, indent=4)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def retreiveAmenityObj(amenity_id):
    """ retrieves a amenity by id """
    amenity = storage.get(amenity, amenity_id).to_dict()
    if amenity is None:
        abort(404)
    return json.dumps(amenity, indent=4)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def createAmenity():
    """ create a amenity """
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a JSON"},
                                        indent=4), 400)
    if "name" not in request.get_json():
        return make_response(json.dumps({"error": "Missing name"},
                                        indent=4), 400)
    new_instance = Amenity(**request.get_json())
    new_instance.save()
    return make_response(json.dumps(new_instance.to_dict(), indent=4), 201)


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """ deletes a amenity by id """
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (json.dumps({}, indent=4))


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """ update a amenity """
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a Json"},
                                        indent=4), 400)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    amenity.save()
    return json.dumps(amenity.to_dict(), indent=4)
