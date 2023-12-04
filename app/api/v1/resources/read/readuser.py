# app/api/v1/resources/read/read.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.models.db import HandlerDB, User
from flask import request, jsonify
from unidecode import unidecode
from app.api.v1.functions.func import check_permissions_read_write, check_key_payload

class ReadUserResource(Resource):
    @jwt_required()
    def get(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data = request.args
            
            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            assert check_permissions_read_write(user), f"El usuario {current_user} esta deshabilitado"

            if check_key_payload(data, 'username'):

                user_to_search = data.get('username', None)

                assert user_to_search, 'Falta el valor username'

                user_found = db.get_data(table=User, column=User.username, find_by=user_to_search, relationship=User.user_permissions)

                assert not isinstance(user_found, str), f"El usuario {unidecode(data['username']).strip().lower()} no existe"

                user_found = user_found.as_dict()
            else:
                assert False, 'payload incorrecto o NO tienes permisos para la acción'

        except Exception as err:
            return {"status": False, "error": str(err)}, 500
        
        return {"status": True, 'result': user_found}, 200