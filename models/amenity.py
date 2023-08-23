#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.place import place_amenity
import models.place  # !NOTE: required for ORM


class Amenity(BaseModel, Base):
    """ Amenity class """
    __tablename__ = "amenities"
    name = Column('name', String(128), nullable=False)
