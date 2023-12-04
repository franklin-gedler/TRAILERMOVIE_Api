# app/api/v1/resources/create/create.py

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from app.api.v1.models.db import HandlerDB, User, Pelicula, Serie
from unidecode import unidecode
from app.api.v1.functions.func import (
    check_permissions_only_write, 
    check_keys_payload_create_pelicula_serie, 
    unpack_values_data_create_pelicula_serie
)

class CreateResource(Resource):
    @jwt_required()
    def post(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data = request.json

            # Obtiene datos del usuario current_user de la base de datos
            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            if check_keys_payload_create_pelicula_serie(data, 'pelicula') or check_keys_payload_create_pelicula_serie(data, 'serie'):

                assert check_permissions_only_write(user), f"El usuario {current_user} No tiene permisos para agregar"

                keys_order = ['video_id', 'link_img', 'details']
            
                if 'name_pelicula' in data:
                    keys_order.insert(2, 'name_pelicula')
                    table = Pelicula
                else:
                    keys_order.insert(2, 'name_serie')
                    table = Serie

                values_order = unpack_values_data_create_pelicula_serie(data=data, keys_order=keys_order, unidecode=unidecode)

                result = db.add_data(table=table, **dict(zip(keys_order, values_order)))

                assert result is True, f'No se pudo agregar la {table.__tablename__[:-1].capitalize()}'

                mje = f'{table.__tablename__[:-1].capitalize()} {values_order[2]} agregada correctamente'

            else:
                assert False, 'payload incorrecto o no tienes permisos para la acción'
                
        except Exception as err:
            return {"status": False, "error": str(err)}, 500
        
        return {"status": True, 'message': mje}, 200