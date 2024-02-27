#!/usr/bin/python3
'''Retrieves Amenity objects'''
from models.amenity import Amenity
import json
from api.v1.views import app_views
from flask import Response, abort, request, jsonify
from models import storage


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    '''Retrieves list of Amenity objects'''
    amenities_list = []
    for key, obj in storage.all(Amenity).items():
        amenities_list.append(obj.to_dict())
    amenity_data = json.dumps(amenities_list, indent=4)
    return Response(
        amenity_data + '\n',
        status=200,
        mimetype="application/json")


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    '''Retrieves an Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity_data = json.dumps(amenity.to_dict(), indent=4)
    return Response(
        amenity_data + '\n',
        status=200,
        mimetype="application/json")


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    '''Deletes an Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return Response(json.dumps({}), 200, mimetype="application/json")


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    '''Creates an Amenity'''
    if not request.is_json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    data = request.get_json()
    new_amenity = Amenity(**data)
    new_amenity.save()
    return Response(json.dumps(new_amenity.to_dict(), indent=4) + '\n', 201,
                    mimetype="application/json")


app_views.route(
    "/amenities/<amenity_id>",
    methods=["PUT"],
    strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates an Ameity object'''
    if not request.is_json:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
