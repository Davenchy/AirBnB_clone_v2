#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return the list of objects of optional one type of class."""
        if not cls:
            return FileStorage.__objects

        if type(cls) == str:
            cls = eval(cls)

        return {k: v for k, v in FileStorage.__objects.items()
                if isinstance(v, cls)}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.objectKey: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            import os
            # A dictionary to map classes names from `str` to `type`
            classes_names = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
                            'City': City, 'Amenity': Amenity, 'State': State,
                            'Review': Review}

            if os.path.exists(FileStorage.__file_path):
                with open(FileStorage.__file_path, 'r') as f:
                    for value in json.load(f).values():
                        # values are dicts
                        # so we need to convert them to instances
                        self.new(classes_names[value['__class__']](**value))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects dict if it's inside."""
        if obj:
            del FileStorage.__objects[obj.objectKey]
