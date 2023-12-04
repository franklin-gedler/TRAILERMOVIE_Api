# app/__init__.py

from flask import Flask
from flask_jwt_extended import JWTManager
from .api import api_v1_blueprint, swaggerui_blueprint
from config.config import Secrets

def create_app():
    app = Flask(__name__)
    app.config.from_object(Secrets)

    # Inicializa Flask-JWT-Extended en la instancia de la aplicación
    jwt = JWTManager(app)

    # Registrar el blueprint de la API
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    # Registrar el blueprint de Swagger UI
    app.register_blueprint(swaggerui_blueprint)

    return app