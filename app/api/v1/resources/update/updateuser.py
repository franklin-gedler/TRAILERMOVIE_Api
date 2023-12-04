# app/api/v1/resources/update/update.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from app.api.v1.models.db import HandlerDB, User, Pelicula, Serie
from unidecode import unidecode
from app.api.v1.functions.func import check_permissions_only_write, is_current_user_super_admin, check_key_payload

class UpdateUserResource(Resource):
    @jwt_required()
    def put(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data_to_search = request.args
            data_to_update = request.json
            
            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            if is_current_user_super_admin(data=data_to_search, user=user):

                user_to_search = unidecode(data_to_search['user']).strip().lower()

                username = data_to_update.get('username', None)
                password = data_to_update.get('password', None)
                allow = data_to_update.get('allow', None)

                assert username is not None or password is not None or allow is not None, 'No se ha enviado ningun dato para actualizar'

                result = db.update_user(user_to_search=user_to_search, username=username, password=password, allow=allow)

                assert isinstance(result, bool), result

                mje = f'Usuario {user_to_search} Actualizado correctamente'

            else:
                assert False, 'payload incorrecto o NO tienes permisos para la acción'
            
        except Exception as err:
            return {"status": False, "error": str(err)}, 500

        return {"status": True, 'message': mje}, 200