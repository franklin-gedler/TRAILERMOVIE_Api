# app/api/v1/resources/read/read.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.models.db import HandlerDB, User, Pelicula, Serie
from flask import request, jsonify
from app.api.v1.functions.func import check_permissions_read_write

class ReadResource(Resource):
    @jwt_required()
    def get(self):
        try:
            find_by = request.args.get('find_by')
            assert find_by is not None, 'Falta el parametro find_by'
            db = HandlerDB()
            current_user = get_jwt_identity()
            
            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            assert check_permissions_read_write(user), f"El usuario {current_user} esta deshabilitado"

            '''data_found = db.get_data(table=Pelicula, column=Pelicula.name_pelicula, find_by=find_by)

            assert not isinstance(data_found, str), data_found

            data_found = data_found.as_dict()'''

            # Buscar en las tablas Pelicula y Serie
            for table_class, column_name in [(Pelicula, Pelicula.name_pelicula), (Serie, Serie.name_serie)]:
                data_found = db.get_data(table=table_class, column=column_name, find_by=find_by)
                if not isinstance(data_found, str):
                    data_found = data_found.as_dict()
                    break
            else:
                assert False, f"No se encontró '{find_by}' en ninguna Pelicula o Serie"

        except Exception as err:
            return {"status": False, "error": str(err)}, 500
        
        return {"status": True, 'result': data_found}, 200