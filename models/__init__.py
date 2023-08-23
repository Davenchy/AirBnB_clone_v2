#!/usr/bin/python3
"""This module instantiates an object of desired storage class."""
from os import environ
from models.utils.classes_injector import ClassesInjector

storage = None
injector = ClassesInjector()
general_injector = ClassesInjector()


def initModelsAndStorage():
    """Inject classes in the injector only once"""
    if getattr(initModelsAndStorage, '__complete__', False):
        return
    setattr(initModelsAndStorage, '__complete__', True)

    from models.base_model import BaseModel, Base
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review

    general_injector.register(Base, BaseModel)
    injector.register(User, Place, State, City, Amenity, Review)

    storage.reload()


if (environ.get('HBNB_TYPE_STORAGE') == 'db'):
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
