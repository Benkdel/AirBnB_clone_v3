#!/usr/bin/python3
"""
    routes for app_views blueprint
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

cls_names = {"Amenity": Amenity, "City": City,
             "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def status():
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def stats():
    dict = {}
    for cls in cls_names:
        count = storage.count(cls)
        dict[cls] = count
    return jsonify(dict)


if __name__ == "__main__":
    pass
