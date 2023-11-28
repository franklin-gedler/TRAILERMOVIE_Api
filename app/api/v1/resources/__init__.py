# app/api/v1/resources/__init__.py

from flask_restful import Api
from .create.create import CreateResource
from .delete.delete import DeleteResource
from .login.login import LoginResource
from .read.read import ReadResource
from .update.update import UpdateResource

api = Api()

api.add_resource(CreateResource, '/create')
api.add_resource(DeleteResource, '/delete')
api.add_resource(LoginResource, '/login')
api.add_resource(ReadResource, '/read')
api.add_resource(UpdateResource, '/update')