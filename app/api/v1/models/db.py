from sqlalchemy import create_engine, Column, String, Text, Integer, TIMESTAMP, or_, inspect, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy import func
from config.config import Secrets
from sqlalchemy.exc import NoSuchTableError, NoResultFound
from datetime import datetime

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
            
            #inspector = inspect(self.engine)
            #assert table.__tablename__ in inspector.get_table_names(), f"La tabla '{table.__tablename__}' no existe en la base de datos"

            #filter_column = getattr(table, column, None)

            #assert column is not None, f'La columna {column} no existe en la tabla {table.__tablename__}'

            #filter_condition = column == find_by
            if isinstance(find_by, str):
                filter_condition = func.lower(column) == func.lower(find_by)
            else:
                filter_condition = column == find_by

            #if relationship is not None and hasattr(table, relationship):
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

    def __del__(self):
        self.session.close()