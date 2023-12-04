# app/api/v1/resources/delete/delete.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from app.api.v1.models.db import HandlerDB, User, Pelicula, Serie
from unidecode import unidecode
from app.api.v1.functions.func import check_permissions_only_write, check_key_payload

class DeleteResource(Resource):
    @jwt_required()
    def delete(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data = request.args

            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            assert check_permissions_only_write(user), f"El usuario {current_user} No tiene permisos para eliminar"

            if check_key_payload(data, 'pelicula') or check_key_payload(data, 'serie'):

                value_pelicula_serie = data.get('pelicula', data.get('serie', None))

                assert value_pelicula_serie, 'falta el nombre pelicula/serie a eliminar'

                if 'pelicula' in data:
                    table = Pelicula
                    column = Pelicula.name_pelicula
                    find_by = unidecode(value_pelicula_serie).strip().capitalize()
                else:
                    table = Serie
                    column = Serie.name_serie
                    find_by = unidecode(value_pelicula_serie).strip().capitalize()

                result = db.delete_data(table=table, column=column, find_by=find_by)

                assert isinstance(result, bool), result

                mje = f'{str(list(data.keys())[0]).capitalize()} {find_by} eliminada correctamente'

            else:
                assert False, 'payload incorrecto o NO tienes permisos para la acción'

        except Exception as err:
            return {"status": False, "error": str(err)}, 500

        return {"status": True, 'message': mje}, 200