#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from models import storage, injector
from models.review import Review
import models.user  # !NOTE: required for ORM
import models.user  # !NOTE required for ORM
from os import environ

place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column('city_id', String(
        60), ForeignKey('cities.id'), nullable=False)
    user_id = Column('user_id', String(
        60), ForeignKey('users.id'), nullable=False)
    name = Column('name', String(128), nullable=False)
    description = Column('description', String(1024), nullable=True)
    number_rooms = Column('number_rooms', Integer, default=0, nullable=False)
    number_bathrooms = Column(
        'number_bathrooms', Integer, default=0, nullable=False)
    max_guest = Column('max_guest', Integer, default=0, nullable=False)
    price_by_night = Column('price_by_night', Integer,
                            default=0, nullable=False)
    latitude = Column('latitude', Float, nullable=True)
    longitude = Column('longitude', Float, nullable=True)
    reviews = relationship(
        'Review', cascade='all, delete, delete-orphan', backref='place')
    amenity_ids = []

    if (environ.get('HBNB_TYPE_STORAG') == 'db'):
        reviews = relationship('Review', cascade='all, delete, delete-orphan',
                               backref='place')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False,
                                 back_populates='place_amenities')
    else:
        @property
        def reviews(self):
            """Get a list of Review instances for the current place."""
            all_reviews = storage.all(Review)
            place_reviews = []
            for review in all_reviews.values():
                if (self.id == review.place_id):
                    place_reviews.append(review)

            return place_reviews

        @property
        def amenities(self):
            """Get a list of Amenity instances for the current place."""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, new_amenity):
            """append new Amenity's id to the attribute amenity_ids."""
            Amenity = injector['Amenity']
            if type(new_amenity) == Amenity:
                if new_amenity.id not in self.amenity_ids:
                    self.amenity_ids.append(new_amenity.id)
