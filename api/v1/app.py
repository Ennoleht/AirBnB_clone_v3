#!/usr/bin/python3
'''REST API'''
import json
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import Response


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    '''Close Storage'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return Response(json.dumps({'error': 'Not found'}, indent=4) + '\n', 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True, debug=True)
