#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models.__init__ import storage
from models.review import Review


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

    @property
    def reviews(self):
        """Get a list of Review instances for the current place."""
        all_reviews = storage.all(Review)
        place_reviews = []
        for review in all_reviews.values():
            if (self.id == review.place_id):
                place_reviews.append(review)

        return place_reviews
