#!/usr/bin/python3
'''Retrieves Place objects'''
from models.place import Place
from models.city import City
from models.user import User
import json
from api.v1.views import app_views
from flask import Response, abort, request
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places(city_id):
	'''Retrieves the list of all Place objects of a City'''
	city = storage.get(City, city_id)
	if not city:
		abort(404)
	place_list = []
	for key, obj in storage.all(Place).items():
		if obj.city_id == city_id:
			place_list.append(obj.to_dict())
	place_data = json.dumps(place_list, indent=4)
	return Response(place_data + '\n', status=200, mimetype="application/json")


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
	'''Retrieves a Place object'''
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	place_data = json.dumps(place.to_dict(), indent=4)
	return Response(place_data + '\n', status=200, mimetype="application/json")

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
	'''Deletes a place object'''
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	storage.delete(place)
	storage.save()
	return Response(json.dumps({}), 200, mimetype="application/json")

@app_views.route("cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
	'''Creates a Place'''
	if not request.json:
		abort(400, "Not a JSON")
	city = storage.get(Place, city_id)
	if not city:
		abort(400)
	if "user_id" not in request.json:
		abort(400, "Missing user_id")
	if "name" not in request.json:
		abort(400, "Missing name")
	data = request.get_json()
	user_id = data["user_id"]
	user = storage.get(Place, user_id)
	if not user:
		abort(400)
	new_place = Place(**data)
	new_place.save()
	return Response(json.dumps(new_place.to_dict(), indent=4) + '\n', 201,
				    mimetype="application/json")

app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
	'''Updates a Place object'''
	if not request.json:
		abort(400, "Not a JSON")
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	data = request.get_json()
	for key, value in data.items():
		if key not in ["id", "created_at", "updated_at"]:
			setattr(place, key, value)
	place.save()
	return Response(json.dumps(place.to_dict(), indent=4) + '\n', 200,
				    mimetype="application/json")
