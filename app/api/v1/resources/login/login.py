from flask_restful import Resource
from flask import request, jsonify
from passlib.context import CryptContext
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.api.v1.models.db import HandlerDB, User
from config.config import Secrets

class LoginResource(Resource):
    def post(self):
        try:
            db = HandlerDB()
            data_user = request.json
            username = data_user.get('username')
            password = data_user.get('password')

            get_user = db.get_data(table=User, column=User.username, find_by=username)

            assert isinstance(get_user, User), 'Usuario no encontrado'

            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

            assert pwd_context.verify(password + get_user.salt, get_user.password_hash), 'Credenciales invalidas'
            
            access_token = create_access_token(identity=username)

        except Exception as err:
            return {"status": False, "error": str(err)}, 500

        return {"status": True, 'access_token': access_token, 'expires': Secrets.JWT_ACCESS_TOKEN_EXPIRES}, 200
        