# app/api/v1/resources/__init__.py

from flask_restful import Api
from .create.create import CreateResource
from .create.createuser import CreateUserResource
from .delete.delete import DeleteResource
from .delete.deleteuser import DeleteUserResource
from .login.login import LoginResource
from .read.read import ReadResource
from .read.readuser import ReadUserResource
from .update.update import UpdateResource
from .update.updateuser import UpdateUserResource
from .spec.spec import SpecResource
from .health.health import HealthResource



api = Api()

api.add_resource(CreateResource, '/create')
api.add_resource(CreateUserResource, '/create/user')
api.add_resource(DeleteResource, '/delete')
api.add_resource(DeleteUserResource, '/delete/user')
api.add_resource(LoginResource, '/login')
api.add_resource(ReadResource, '/read')
api.add_resource(ReadUserResource, '/read/user')
api.add_resource(UpdateResource, '/update')
api.add_resource(UpdateUserResource, '/update/user')
api.add_resource(SpecResource, '/spec')
api.add_resource(HealthResource, '/health')