#!/usr/bin/python3
'''
View for the link between Place objects and Amenity objects
that handles all default RESTFul API actions.
'''
from os import getenv
from models.place import Place
from models.amenity import Amenity
import json
from api.v1.views import app_views
from flask import Response, abort, request
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
				 strict_slashes=False)
def get_place_amenities(place_id):
	'''Retrieves list of place amenities'''
	amenity_list = []
	place = storage.all(Place, place_id)
	if not place:
		abort(404)
	if getenv("HBNB_TYPE_STORAGE") == "db":
		amenity_list = [amenity.to_dict() for amenity in place.amenities]
	else:
		amenity_list = [storage.get(Amenity, amenity_id).to_dict() for
				  		amenity_id in place.amenity_ids]
	amenity_data = json.dumps(amenity_list, indent=4)
	return Response(amenity_data + '\n', status=200, mimetype="application/json")


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def get_amenity(place_id, amenity_id):
	'''Retrieves a Amenity object'''
	state = storage.get(State, state_id)
	if not state:
		abort(404)
	state_data = json.dumps(state.to_dict(), indent=4)
	return Response(state_data + '\n', status=200, mimetype="application/json")

@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
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

app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
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
	return Response(json.dumps(state.to_dict(), indent=4) + '\n', 200,
				    mimetype="application/json")
