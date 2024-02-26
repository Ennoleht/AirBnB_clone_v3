#!/usr/bin/python3
'''
Module containing class BaseModel
that defines all common attributes/methods for other classes.
'''
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv


Base = declarative_base()


class BaseModel:
    '''BaseModel class'''
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), primary_key=True,
                    default=uuid.uuid4, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    else:
        id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()

    def __init__(self, *args, **kwargs):
        '''Instantiation method.'''
        if kwargs:
            self.__dict__.update(kwargs)
            if self.__dict__.get("__class__"):
                del self.__dict__["__class__"]
            if self.__dict__.get("created_at", None):
                self.__dict__["created_at"] = \
                    datetime.strptime(self.__dict__["created_at"],
                                      "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.__dict__["created_at"] = datetime.utcnow()

            if self.__dict__.get("updated_at", None):
                self.__dict__["updated_at"] = \
                    datetime.strptime(self.__dict__["updated_at"],
                                      "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.__dict__["updated_at"] = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        '''
        Prints string representation of Class
        in the format [<class name>] (<self.id>) <self.__dict__>.
        '''
        class_name = self.__class__.__name__
        dictionary = {}
        dictionary.update(self.__dict__)
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            if dictionary.get("_sa_instance_state"):
                del dictionary["_sa_instance_state"]
        return (f"[{class_name}] ({self.id}) {dictionary}")

    def save(self):
        from models import storage
        '''
        updates the public instance attribute
        updated_at with the current datetime
        '''
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        '''
        returns a dictionary containing all keys/values
        of __dict__ of the instance.
        '''
        dictionary = {}
        dictionary.update(self.__dict__)
        if dictionary.get("id"):
            dictionary["id"] = str(dictionary["id"])
        dictionary["__class__"] = self.__class__.__name__
        if dictionary.get("_sa_instance_state"):
            del dictionary["_sa_instance_state"]
        dictionary["updated_at"] = self.updated_at.isoformat()
        dictionary["created_at"] = self.created_at.isoformat()
        return dictionary

    def delete(self):
        from models import storage
        '''
        Deletes the current instance from the storage.
        '''
        storage.delete(self)
