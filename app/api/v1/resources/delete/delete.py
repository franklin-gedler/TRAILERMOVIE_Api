# app/api/v1/resources/delete/delete.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required

class DeleteResource(Resource):
    @jwt_required()
    def delete(self):
        # Lógica para eliminar el recurso protegido por JWT
        return {'message': 'Recurso eliminado correctamente'}, 200
