# app/api/v1/resources/delete/delete.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.api.v1.models.db import HandlerDB, User
from unidecode import unidecode
from app.api.v1.functions.func import is_current_user_super_admin

class DeleteUserResource(Resource):
    @jwt_required()
    def delete(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data = request.args

            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            if is_current_user_super_admin(data=data, user=user):
                
                assert data.get('user', None), 'falta el usuario a eliminar'

                user_to_del = unidecode(data['user']).strip().lower()

                assert user_to_del != current_user, f'Usuario {current_user} no puede eliminarse a si mismo'

                result = db.delete_user(table=User, column=User.username, find_by=user_to_del)

                assert isinstance(result, bool), result

                mje = f'Usuario {user_to_del} eliminado correctamente'

            else:
                assert False, 'payload incorrecto o NO tienes permisos para la acción'

        except Exception as err:
            return {"status": False, "error": str(err)}, 500

        return {"status": True, 'message': mje}, 200