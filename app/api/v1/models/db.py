from sqlalchemy import create_engine, Column, String, Text, Integer, TIMESTAMP, or_, inspect, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy import func
from config.config import Secrets
from sqlalchemy.exc import NoSuchTableError, NoResultFound
from datetime import datetime
from unidecode import unidecode

Base = declarative_base()

class Pelicula(Base):
    __tablename__ = 'peliculas'
    id = Column(Integer, primary_key=True)
    video_id = Column(String(255), nullable=False)
    link_img = Column(String(255), nullable=False)
    name_pelicula = Column(String(255), nullable=False)
    details = Column(Text, nullable=False)
    total_average = Column(String(255))
    vote_count = Column(Integer)
    #created_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    def as_dict(self):
        #return {column.key: getattr(self, column.key) for column in self.__table__.columns}
        data = {column.key: getattr(self, column.key) for column in self.__table__.columns}
        data['created_at'] = data['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return data

class Serie(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    video_id = Column(String(255), nullable=False)
    link_img = Column(String(255), nullable=False)
    name_serie = Column(String(255), nullable=False)
    details = Column(Text, nullable=False)
    total_average = Column(String(255))
    vote_count = Column(Integer)
    #created_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    def as_dict(self):
        #return {column.key: getattr(self, column.key) for column in self.__table__.columns}
        data = {column.key: getattr(self, column.key) for column in self.__table__.columns}
        data['created_at'] = data['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return data

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    user_permissions = relationship('UserPermission', backref='user')

    def as_dict(self):
        excluded_columns = ['password_hash', 'salt']
        data = {column.key: getattr(self, column.key) for column in self.__table__.columns if column.key not in excluded_columns}
        data['created_at'] = data['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        data['updated_at'] = data['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        # Agregar datos de la relación User.user_permissions
        user_permissions = []
        for user_permission in self.user_permissions:
            user_permission_data = {column.key: getattr(user_permission, column.key) for column in user_permission.__table__.columns}

            # Modificar el valor de permission_id según las condiciones
            if 'permission_id' in user_permission_data:
                permission_id = user_permission_data['permission_id']
                if permission_id == 1:
                    user_permission_data['permission_id'] = 'read'
                elif permission_id == 2:
                    user_permission_data['permission_id'] = 'write'
                elif permission_id == 3:
                    user_permission_data['permission_id'] = 'disable'

            user_permissions.append(user_permission_data)

        data['user_permissions'] = user_permissions

        return data

class UserPermission(Base):
    __tablename__ = 'userpermissions'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

class HandlerDB:
    def __init__(self):
        self.engine = create_engine(Secrets.DB_CONFIG)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_data(self, table = None, column = None, find_by = None, relationship = None):
        try:
            
            if isinstance(find_by, str):
                #filter_condition = func.lower(column) == func.lower(find_by)
                filter_condition = func.lower(func.trim(column)) == unidecode(find_by).lower().strip()
            else:
                filter_condition = column == find_by

            if relationship is not None:
                result = self.session.query(table).filter(filter_condition).options(joinedload(relationship)).first()
            else:
                result = self.session.query(table).filter(filter_condition).first()

            assert result is not None, f"No se encontró el '{find_by}' en la tabla '{table.__tablename__}'"

            return result
        
        except AssertionError as err:
            return str(err)
        
    def add_data(self, table = None, **kwargs):
        try:
            #inspector = inspect(self.engine)
            #assert table.__tablename__ in inspector.get_table_names(), f"La tabla '{table.__tablename__}' no existe en la base de datos"

            self.session.add(table(**kwargs))
            self.session.commit()

            return True
        
        except AssertionError as err:
            return str(err)
        
    def add_user(self, username, password, allow):
        try:
            # Ejecutar la función hash_password directamente con una consulta SQL
            query = text(f"SELECT hash_password('{username}', '{password}', '{allow}')")
            self.session.execute(query)
            self.session.commit()

            return True

        except Exception as err:
            return str(err)
        
    def delete_user(self, table=None, column=None, find_by=None):
        try:
            user = self.get_data(table=table, column=column, find_by=find_by, relationship=User.user_permissions)

            # Verificar si se encontró el usuario
            assert not isinstance(user, str), f'Usuario {find_by} no existe'

            # Eliminar relaciones en la tabla UserPermission
            for user_permission in user.user_permissions:
                self.session.delete(user_permission)

            # Eliminar el usuario
            self.session.delete(user)
            self.session.commit()

            return True

        except AssertionError as err:
            return str(err)
        
    def delete_data(self, table=None, column=None, find_by=None):
        try:
            data = self.get_data(table=table, column=column, find_by=find_by)

            # Verificar si se encontró el dato
            assert not isinstance(data, str), f'{find_by} no existe en {table.__tablename__.capitalize()}'

            # Eliminar el dato
            self.session.delete(data)
            self.session.commit()

            return True

        except AssertionError as err:
            return str(err)
        
    def update_data(self, table=None, **kwargs):
        try:
        
            # Actualizar las columnas con los nuevos valores
            for column, value in kwargs.items():
                if column == 'name_pelicula' or column == 'name_serie':
                    setattr(table, column, unidecode(value).strip().capitalize())
                else:
                    setattr(table, column, value.strip())

            self.session.commit()

            return True

        except Exception as err:
            return str(err)

    def update_user(self, user_to_search, username=None, password=None, allow=None):
        try:

            user = self.get_data(table=User, column=User.username, find_by=user_to_search, relationship=User.user_permissions)

            # Verificar si se encontró el usuario
            assert not isinstance(user, str), f'Usuario {user_to_search} no existe'

            # Valido si username no exista para evitar nombres repetidos
            if username is not None:
                user = self.get_data(table=User, column=User.username, find_by=username, relationship=User.user_permissions)
                assert isinstance(user, str), f'El new name {username} ya existe'

            # Utilizar el operador ternario para cambiar None a NULL en la consulta SQL
            username = f"'{username}'" if username is not None else "NULL"
            password = f"'{password}'" if password is not None else "NULL"
            allow = f"'{allow}'" if allow is not None else "NULL"


            query = text(f"SELECT update_user('{user_to_search}', {username}, {password}, {allow})")
            self.session.execute(query)
            self.session.commit()

            return True

        except Exception as err:
            return str(err)

    def __del__(self):
        self.session.close()