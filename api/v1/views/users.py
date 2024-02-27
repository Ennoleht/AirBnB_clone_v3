#!/usr/bin/python3
'''Retrieves User objects'''
from models.user import User
import json
from api.v1.views import app_views
from flask import Response, abort, request, jsonify
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    '''Retrieves list of User objects'''
    user_list = []
    for key, obj in storage.all(User).items():
        user_list.append(obj.to_dict())
    state_data = json.dumps(user_list, indent=4)
    return Response(state_data + '\n', status=200, mimetype="application/json")


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    '''Retrieves a User object'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_data = json.dumps(user.to_dict(), indent=4)
    return Response(user_data + '\n', status=200, mimetype="application/json")


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    '''Deletes a User object'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return Response(json.dumps({}), 200, mimetype="application/json")


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    '''Creates a User'''
    if not request.is_json:
        abort(400, "Not a JSON")
    if "email" not in request.json:
        abort(400, "Missing email")
    if "password" not in request.json:
        abort(400, "Missing password")
    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return Response(json.dumps(new_user.to_dict(), indent=4) + '\n', 201,
                    mimetype="application/json")


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    '''Updates a User object'''
    if not request.is_json:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
