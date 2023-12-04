# app/api/v1/resources/create/create.py

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.api.v1.models.db import HandlerDB, User
from unidecode import unidecode
from app.api.v1.functions.func import (
    check_keys_payload_user_create, 
    unpack_values_data_create_user
)

class CreateUserResource(Resource):
    @jwt_required()
    def post(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data = request.json

            # Obtiene datos del usuario current_user de la base de datos
            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            # Valida si el current_user es id = 1 y valida si el payload recibido tiene la keys username, password y allow
            if check_keys_payload_user_create(data, user):

                # validar si el value de username no existe en la base de datos
                user_found = db.get_data(table=User, column=User.username, find_by=unidecode(data['username']).strip().lower())

                assert isinstance(user_found, str), f"El usuario {unidecode(data['username']).strip().lower()} ya existe"

                keys_order = ['username', 'password', 'allow']
                values_order = unpack_values_data_create_user(data=data, keys_order=keys_order, unidecode=unidecode)

                username, password, allow = values_order

                result = db.add_user(username=username, password=password, allow=allow)

                assert result is True, 'No se pudo crear el usuario'

                mje = f'Usuario {username} creado correctamente'
            
            else:
                assert False, 'payload incorrecto o no tienes permisos para la acción'
                
        except Exception as err:
            return {"status": False, "error": str(err)}, 500
        
        return {"status": True, 'message': mje}, 200