'''
Created on 19 Aug 2014

@author: tufyx
'''
from flask import Flask, request
from functools import update_wrapper
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
cors = CORS(app)
app.config.from_pyfile("config.py", False)
db = SQLAlchemy(app)

from app import views, models

@app.after_request
def add_cors(response):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, DELETE'
    response.headers['Access-Control-Allow-Headers'] = request.headers.get( 'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        response.headers['Access-Control-Max-Age'] = '1'
    return response