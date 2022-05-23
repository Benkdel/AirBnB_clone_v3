#!/usr/bin/python3
"""
    reviews views
"""

import json
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from flask import abort, make_response, request


@app_views.route("/states/<string:place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def retreiveReviews(place_id):
    """ get list of reviews from place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return json.dumps(reviews, indent=4)


@app_views.route("/reviews/<string:review_id>", methods=["GET"],
                 strict_slashes=False)
def retreiveReview(review_id):
    """ get review by id """
    review = storage.get(Review, review_id).to_dict()
    if review is None:
        abort(404)
    return json.dumps(review, indent=4)


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def createReview(place_id):
    """ create a review """
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a JSON"},
                                        indent=4), 400)
    if "name" not in request.get_json():
        return make_response(json.dumps({"error": "Missing name"},
                                        indent=4), 400)
    place = storage.get(Place, place_id).to_dict()
    if place is None:
        abort(404)
    dict = request.get_json()
    dict["place_id"] = place_id
    new_instance = Review(**dict)
    new_instance.save()
    return make_response(json.dumps(new_instance.to_dict(),
                                    indent=4), 201)


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteReview(review_id):
    """ deletes a review by id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return (json.dumps({}, indent=4))


@app_views.route("/reviews/<string:review_id>", methods=["PUT"],
                 strict_slashes=False)
def updateReview(review_id):
    """ update a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(json.dumps({"error": "Not a Json"},
                                        indent=4), 400)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, val)
    review.save()
    return json.dumps(review.to_dict(), indent=4)
