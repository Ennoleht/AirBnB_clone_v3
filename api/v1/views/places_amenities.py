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
from flask import Response, abort, request, jsonify
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    '''Retrieves list of place amenities'''
    amenity_list = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenity_list = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenity_list = [storage.get(Amenity, amenity_id).to_dict() for
                        amenity_id in place.amenity_ids]
    amenity_data = json.dumps(amenity_list, indent=4)
    return Response(
        amenity_data + '\n',
        status=200,
        mimetype="application/json")


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object of a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return Response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return Response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return Response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return Response(jsonify(amenity.to_dict()), 201)
