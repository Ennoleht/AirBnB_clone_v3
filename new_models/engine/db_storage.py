#!/usr/bin/python3
'''Module containing DBStorage Class'''
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

user = getenv('HBNB_MYSQL_USER')
password = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
db = getenv('HBNB_MYSQL_DB')


class DBStorage:
    '''Engine to handle database storage'''
    __engine = None
    __session = None

    def __init__(self):
        '''Starts engine'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        Returns a dictionary containing objects
        Key = <class-name>.<object-id>
        Value = object
        '''
        obj_dict = {}
        classes = [City, State, User, Place, Review, Amenity]

        if cls:
            if type(cls) is str:
                cls = eval(cls)
            if cls in classes:
                objects = self.__session.query(cls).all()
                for obj in objects:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    value = obj
                    obj_dict[key] = value
        else:
            for cls in classes:
                objects = self.__session.query(cls).all()
                for obj in objects:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    value = obj
                    obj_dict[key] = value
        return obj_dict

    def new(self, obj):
        '''Adds new object to current db session'''
        self.__session.add(obj)

    def save(self):
        '''Commit all changes of current db session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''
        Delete from the current database session obj if not None.
        '''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''Create all tables in the database'''
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()
    
    def close(self):
        '''
        Call remove() method
        on the private session attribute (self.__session).
        '''
        self.__session.close()

    def get(self, cls, id):
        '''
        cls: class
        id: string representing the object ID
        Returns the object based on the class and its ID,
        or None if not found.
        '''
        for key, obj in self.all(cls).items():
            if obj.id == id:
                return obj
        return None
    
    def count(self, cls=None):
        '''
        A method to count the number of objects in storage:
        cls: class (optional)
        Returns the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage.
        '''
        return len(self.all(cls if cls else None))
