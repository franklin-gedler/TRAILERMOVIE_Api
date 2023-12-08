from flask_restful import Resource
from flask import request, make_response
from passlib.context import CryptContext
from flask_jwt_extended import create_access_token
from app.api.v1.models.db import HandlerDB, User
from config.config import Static
from app.api.v1.functions.func import check_user_disable

class LoginResource(Resource):
    def post(self):
        try:
            db = HandlerDB()
            data_user = request.json
            username = data_user.get('username', None)
            password = data_user.get('password', None)

            assert username is not None or password is not None, 'payload invalido'

            get_user = db.get_data(table=User, column=User.username, find_by=username, relationship=User.user_permissions)

            assert isinstance(get_user, User), 'Usuario no encontrado'

            id_permission_user = check_user_disable(user=get_user)

            assert id_permission_user, 'Usuario deshabilitado'

            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

            assert pwd_context.verify(password + get_user.salt, get_user.password_hash), 'Credenciales invalidas'
            
            access_token = create_access_token(identity=username)

        except Exception as err:
            return {"status": False, "error": str(err)}, 500
        
        resp = {"status": True, 'access_token': access_token, 'expires': Static.JWT_ACCESS_TOKEN_EXPIRES}
        resp = make_response(resp, 200)
        resp.headers['X-User-Role'] = id_permission_user

        return resp
        