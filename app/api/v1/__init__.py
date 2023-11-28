# app/api/v1/__init__.py

from flask import Blueprint
from .resources import api

api_v1_blueprint = Blueprint('api_v1', __name__)

api.init_app(api_v1_blueprint)
