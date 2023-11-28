# app/api/v1/resources/create/create.py

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from app.api.v1.models.db import HandlerDB, User, Pelicula, Serie
from app.api.v1.functions.func import check_keys_payload_user, check_keys_payload_pelicula_serie, check_permissions_only_write

class CreateResource(Resource):
    @jwt_required()
    def post(self):
        try:
            db = HandlerDB()
            current_user = get_jwt_identity()
            data = request.json

            user = db.get_data(table=User, column=User.username, find_by=current_user, relationship=User.user_permissions)

            if check_keys_payload_user(data, user):

                username, password, allow = data['user'].values()

                result = db.add_user(username=username, password=password, allow=allow)

                assert result is True, 'No se pudo crear el usuario'

                mje = f'Usuario {username} creado correctamente'
            
            elif check_keys_payload_pelicula_serie(data, 'pelicula'):
            
                assert check_permissions_only_write(user), f"El usuario {current_user} No tienes permisos para agregar"

                video_id, link_img, name_pelicula, details = data['pelicula'].values()

                result = db.add_data(table=Pelicula, video_id=video_id, link_img=link_img, name_pelicula=name_pelicula, details=details)

                assert result is True, 'No se pudo agregar la pelicula'

                mje = f'Pelicula {name_pelicula} agregada correctamente'
            
            elif check_keys_payload_pelicula_serie(data, 'serie'):
                #assert user.user_permissions[0].permission_id == 2, f"El usuario {current_user} No tienes permisos para agregar"

                assert check_permissions_only_write(user), f"El usuario {current_user} No tienes permisos para agregar"

                video_id, link_img, name_serie, details = data['serie'].values()

                result = db.add_data(table=Serie, video_id=video_id, link_img=link_img, name_serie=name_serie, details=details)

                assert result is True, 'No se pudo agregar la serie'

                mje = f'Serie {name_serie} agregada correctamente'

            else:
                assert False, 'payload incorrecto o no tienes permisos para la acción'
                
        except Exception as err:
            return {"status": False, "error": str(err)}, 500
        
        return {"status": True, 'message': mje}, 200
