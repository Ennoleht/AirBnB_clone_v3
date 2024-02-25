#!/usr/bin/python3
'''Index API handler'''
import json
from api.v1.views import app_views
from flask import Response
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    '''Returns app status'''
    status = json.dumps({"status": "OK"}, indent=4)
    return Response(status + '\n', status=200, mimetype="application/json")


@app_views.route("/stats", methods=["GET"])
def stats():
    '''Returns stats'''
    names = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"}
    stats = {}
    for key in names.keys():
        stats[names[key]] = storage.count(key)
        data = json.dumps(stats, indent=4)
    return Response(data + '\n', status=200, mimetype="application/json")


@app_views.route("/nop", methods=["GET"])
def not_found():
    '''
    Create a handler for 404 errors that returns a
    JSON-formatted 404 status code response.
    '''
    status = json.dumps({"error": "Not found"}, indent=4)
    return Response(status + '\n', status=200, mimetype="application/json")
