#!/usr/bin/python3
'''Module containing Place Class'''
from os import getenv
from models.base_model import BaseModel, Base, Column, String
from sqlalchemy import Integer, ForeignKey, Float, Table
from sqlalchemy.orm import Relationship
from models.review import Review

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 nullable=False))

if getenv('HBNB_TYPE_STORAGE') == 'db':
    class Place(BaseModel, Base):
        '''Place Class'''
        __tablename__ = "places"
        city_id: str = Column(String(60), ForeignKey("cities.id"),
                              nullable=False)
        user_id: str = Column(String(60), ForeignKey("users.id"),
                              nullable=False)
        name: str = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms: int = Column(Integer, nullable=False, default=0)
        number_bathrooms: int = Column(Integer, nullable=False, default=0)
        max_guest: int = Column(Integer, nullable=False, default=0)
        price_by_night: int = Column(Integer, nullable=False, default=0)
        latitude: float = Column(Float)
        longitude: float = Column(Float)
        amenity_ids: list = []
        # Create one-to-many relationship with Review
        reviews = Relationship("Review", backref="place",
                               cascade="all, delete-orphan")
        # Ceate many-to-many relationship with Amenities
        amenities = Relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)
else:
    class Place(BaseModel):
        '''Place Class'''
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            '''Include relationship if storage is not db'''
            from models import storage

            obj_list = []
            for key, obj in storage.all(Review).items():
                if obj.place_id == self.id:
                    obj_list.append(obj)
            return obj_list

        @property
        def amenities(self):
            '''
            Returns the list of Amenity instances
            based on the attribute amenity_ids that contains all Amenity.id
            linked to the Place.
            '''
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            from models.amenity import Amenity
            '''
            Handles append method for adding an Amenity.id
            to the attribute amenity_ids. This method should accept
            only Amenity object, otherwise, do nothing.
            '''
            if obj and obj.__class__.__name__ == "Amenity":
                self.amenity_ids.append(obj.id)
