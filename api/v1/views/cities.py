#!/usr/bin/python3
'''Retrieves city objects'''

from models.city import City
from models.state import State
import json
from api.v1.views import app_views
from flask import Response, abort, request, jsonify
from models import storage


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    '''Retrieves list of City object of a State'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_list = []
    for key, obj in storage.all(City).items():
        if obj.state_id == state_id:
            city_list.append(obj.to_dict())
    city_data = json.dumps(city_list, indent=4)
    return Response(city_data + '\n', status=200, mimetype="application/json")


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    '''Retrieves a City object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city_data = json.dumps(city.to_dict(), indent=4)
    return Response(city_data + '\n', status=200, mimetype="application/json")


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    '''Deletes a city object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return Response(json.dumps({}), 200, mimetype="application/json")


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def create_city(state_id):
    '''Creates a City'''
    if not request.is_json:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if "name" not in request.json:
        abort(400, "Missing Name")
    data = request.get_json()
    new_city = City(**data)
    setattr(new_city, "state_id", state_id)
    new_city.save()
    return Response(json.dumps(new_city.to_dict(), indent=4) + '\n', 201,
                    mimetype="application/json")


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    '''Updates a city object'''
    if not request.is_json:
        abort(400, "Not a JSON")

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
