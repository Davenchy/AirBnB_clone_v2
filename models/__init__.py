#!/usr/bin/python3
"""This module instantiates an object of desired storage class."""

from models.engine.db_storage import DBStorage, DB_TYPE
from models.engine.file_storage import FileStorage

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


tables = {'State', 'City', 'Place', 'User', 'Review', 'Amenity'}
classes = {
    'BaseModel': BaseModel, 'User': User, 'Place': Place, 'State': State,
    'City': City, 'Amenity': Amenity, 'Review': Review,
}


if (DB_TYPE == 'db'):
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
