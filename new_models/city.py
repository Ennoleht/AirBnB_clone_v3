#!/usr/bin/python3
'''Module containing City Class'''
from models.base_model import BaseModel, Base, Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Relationship
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    class City(BaseModel, Base):
        '''City Class'''
        __tablename__ = "cities"
        name: str = Column(String(128), nullable=False)
        # Define foeign key
        state_id: str = Column(String(60),
                               ForeignKey('states.id'), nullable=False)
        # One to many relationship with Place
        places = Relationship("Place",
                              backref="cities", cascade="all, delete-orphan")
else:
    class City(BaseModel):
        '''City Class'''
        state_id = ""
        name = ""
