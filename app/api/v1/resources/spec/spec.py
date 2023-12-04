# app/api/v1/resources/spec/spec.py

from flask import current_app, jsonify
from flask_restful import Resource
import json

class SpecResource(Resource):
    def get(self):
        try:
            # Cargar la especificación Swagger desde un archivo local
            with current_app.open_resource('api/v1/resources/spec/swagger.json', 'r') as file:
                swagger_spec = json.loads(file.read())

            return jsonify(swagger_spec)
        
        except Exception as err:
            return {"status": False, "error": str(err)}, 500
