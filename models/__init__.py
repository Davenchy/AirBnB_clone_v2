#!/usr/bin/python3
"""This module instantiates an object of desired storage class."""
from os import environ
from models.utils.classes_injector import ClassesInjector

storage = None
injector = ClassesInjector()


def injectClasses():
    """Inject classes in the injector only once"""
    if getattr(injectClasses, '__complete__', False):
        return
    setattr(injectClasses, '__complete__', True)

    from models.base_model import BaseModel
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review

    injector.register(BaseModel, User, Place,
                      State, City, Amenity, Review,)


if (environ.get('HBNB_TYPE_STORAGE') == 'db'):
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
