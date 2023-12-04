# app/api/v1/__init__.py

from flask import Blueprint
from .resources import api
from flask_swagger_ui import get_swaggerui_blueprint
from config.config import Static

api_v1_blueprint = Blueprint('api_v1', __name__)

api.init_app(api_v1_blueprint)

swaggerui_blueprint = get_swaggerui_blueprint(
    base_url=Static.SWAGGER_URL,
    api_url=Static.API_URL,
    config=Static.CONFIG_SWAGGER
)