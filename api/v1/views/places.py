#!/usr/bin/python3
'''Retrieves Place objects'''
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
import json
from api.v1.views import app_views
from flask import Response, abort, request, jsonify
from models import storage


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
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


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    '''Deletes a place object'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return Response(json.dumps({}), 200, mimetype="application/json")


@app_views.route("cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    '''Creates a Place'''
    if not request.is_json:
        abort(400, "Not a JSON")
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    if "name" not in request.json:
        abort(400, "Missing name")
    data = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    user_id = data["user_id"]
    data["city_id"] = city_id
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    new_place = Place(**data)
    new_place.save()
    return Response(json.dumps(new_place.to_dict(), indent=4) + '\n', 201,
                    mimetype="application/json")


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    '''Updates a Place object'''
    if not request.is_json:
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
