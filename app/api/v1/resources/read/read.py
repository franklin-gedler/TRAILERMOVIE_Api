# app/api/v1/resources/read/read.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.models.db import HandlerDB, User, Pelicula, Serie
from flask import request, jsonify
from app.api.v1.functions.func import check_permissions_read_write, check_key_payload

class ReadResource(Resource):
    @jwt_required()
    def get(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data = request.args
            
            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            assert check_permissions_read_write(user), f"El usuario {current_user} esta deshabilitado"

            if check_key_payload(data, 'name'):

                name = request.args.get('name', None)

                assert name, 'Falta el valor name'

                # Buscar en las tablas Pelicula y Serie
                for table_class, column_name in [(Pelicula, Pelicula.name_pelicula), (Serie, Serie.name_serie)]:
                    data_found = db.get_data(table=table_class, column=column_name, find_by=name)
                    if not isinstance(data_found, str):
                        data_found = data_found.as_dict()
                        break
                else:
                    assert False, f"No se encontró '{name}' en Pelicula o Serie"

            else:
                assert False, 'payload incorrecto o NO tienes permisos para la acción'

        except Exception as err:
            return {"status": False, "error": str(err)}, 500
        
        return {"status": True, 'result': data_found}, 200