#!/usr/bin/python3
'''Retrieves state objects'''
from models.state import State
import json
from api.v1.views import app_views
from flask import Response, abort, request, jsonify
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    '''Retrieves list of state object'''
    state_list = []
    for key, obj in storage.all(State).items():
        state_list.append(obj.to_dict())
    state_data = json.dumps(state_list, indent=4)
    return Response(state_data + '\n', status=200, mimetype="application/json")


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    '''Retrieves a State object'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_data = json.dumps(state.to_dict(), indent=4)
    return Response(state_data + '\n', status=200, mimetype="application/json")


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    '''Deletes a state object'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return Response(json.dumps({}), 200, mimetype="application/json")


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    '''Creates a State'''
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing Name")
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return Response(json.dumps(new_state.to_dict(), indent=4) + '\n', 201,
                    mimetype="application/json")


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    '''Updates a state object'''
    if not request.json:
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
