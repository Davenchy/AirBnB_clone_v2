#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.utils.consts import DB_TYPE


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column('name', String(128), nullable=False)

    if DB_TYPE == 'db':
        cities = relationship(
            'City', cascade='all, delete, delete-orphan', backref='state')
    else:
        @property
        def cities(self):
            """Return the list of City instances in current state."""
            state_cities = []

            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if (self.id == city.state_id):
                    state_cities.append(city)

            return state_cities
