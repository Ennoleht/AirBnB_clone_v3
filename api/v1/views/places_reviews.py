#!/usr/bin/python3
'''View for Review object that handles all default RESTFul API actions'''
from models.place import Place
from models.user import User
from models.review import Review
from models.state import State
import json
from api.v1.views import app_views
from flask import Response, abort, request
from models import storage


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    '''Retrieves the list of all Review objects of a Place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_list = []
    for key, obj in storage.all(Review).items():
        if obj.place_id == place_id:
            review_list.append(obj.to_dict())
    review_data = json.dumps(review_list, indent=4)
    return Response(
        review_data + '\n',
        status=200,
        mimetype="application/json")


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    '''Retrieves a Review object'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review_data = json.dumps(review.to_dict(), indent=4)
    return Response(
        review_data + '\n',
        status=200,
        mimetype="application/json")


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    '''Deletes a review object'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return Response(json.dumps({}), 200, mimetype="application/json")


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    '''Creates a Review'''
    if not request.is_json:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    if "text" not in request.json:
        abort(400, "Missing text")
    data = request.get_json()
    user_id = data["user_id"]
    data["place_id"] = place_id
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    new_review = Review(**data)
    new_review.save()
    return Response(json.dumps(new_review.to_dict(), indent=4) + '\n', 201,
                    mimetype="application/json")


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    '''Updates a review object'''
    if not request.is_json:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return Response(json.dumps(review.to_dict(), indent=4) + '\n', 200,
                    mimetype="application/json")
