#!/usr/bin/python3
'''Module containing User Class'''
from models.base_model import BaseModel, Base, Column, String
from sqlalchemy.orm import Relationship
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    class User(BaseModel, Base):
        '''User Class'''
        __tablename__ = "users"
        email: str = Column(String(128), nullable=False)
        password: str = Column(String(128), nullable=False)
        first_name: str = Column(String(128))
        last_name: str = Column(String(128))
        # One to many relationship with Place
        places = Relationship("Place", backref="user",
                              cascade="all, delete-orphan")
        # One to many relationship with Review
        reviews = Relationship("Review", backref="user",
                               cascade="all, delete-orphan")
else:
    class User(BaseModel):
        '''User Class'''
        email = ""
        password = ""
        first_name = ""
        last_name = ""
