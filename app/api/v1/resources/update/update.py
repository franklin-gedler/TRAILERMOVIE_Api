# app/api/v1/resources/update/update.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required

class UpdateResource(Resource):
    @jwt_required()
    def put(self):
        # Lógica para actualizar el recurso protegido por JWT
        return {'message': 'Recurso actualizado correctamente'}, 200
