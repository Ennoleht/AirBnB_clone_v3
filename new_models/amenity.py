#!/usr/bin/python3
'''Module containing Amenity Class'''
from os import getenv
from models.base_model import BaseModel, Base, Column, String
from sqlalchemy.orm import Relationship


if getenv('HBNB_TYPE_STORAGE') == 'db':
    class Amenity(BaseModel, Base):
        from models.place import place_amenity
        '''Amenity Class'''
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        place_amenities = Relationship("Place", secondary=place_amenity,
                                       viewonly=False, overlaps="amenities")
else:
    class Amenity(BaseModel):
        '''Amenity Class'''
        name = ""
