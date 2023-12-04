# app/api/v1/resources/update/update.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from app.api.v1.models.db import HandlerDB, User, Pelicula, Serie
from unidecode import unidecode
from app.api.v1.functions.func import check_permissions_only_write, is_current_user_super_admin, check_key_payload
class UpdateResource(Resource):
    @jwt_required()
    def put(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data_to_update = request.json
            data_to_search = request.args

            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            if check_key_payload(data_to_search, 'name'):

                assert check_permissions_only_write(user), f"El usuario {current_user} No tiene permisos para Actualizar"

                find_by = unidecode(data_to_search.get('name').capitalize().strip())

                # Buscar en las tablas Pelicula y Serie
                for table_class, column_name in [(Pelicula, Pelicula.name_pelicula), (Serie, Serie.name_serie)]:
                    data_found = db.get_data(table=table_class, column=column_name, find_by=find_by)
                    if not isinstance(data_found, str):
                        table_found_name = data_found.__tablename__
                        break
                else:
                    assert False, f"No se encontró '{find_by}' en Pelicula o Serie"

                # Si existe 'new_name' se reemplaza por 'name_pelicula' o 'name_serie'
                if 'new_name' in data_to_update:
                    if table_found_name == 'peliculas':
                        data_to_update['name_pelicula'] = data_to_update.pop('new_name')
                    else:
                        data_to_update['name_serie'] = data_to_update.pop('new_name')

                result = db.update_data(table=data_found, **dict(zip(data_to_update.keys(), data_to_update.values())))

                assert isinstance(result, bool), result

                mje = f'{table_found_name[:-1].capitalize()} {find_by.capitalize()} Actualizada correctamente'

            else:
                assert False, 'param incorrecto o NO tienes permisos para la acción'
            
        except Exception as err:
            return {"status": False, "error": str(err)}, 500

        return {"status": True, 'message': mje}, 200