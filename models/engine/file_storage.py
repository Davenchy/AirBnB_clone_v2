#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models import injector


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return the list of objects of optional one type of class."""
        if not cls:
            return FileStorage.__objects
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
        # load injected classes
        classes = injector.classes
        print("reloading database")
        print("injected classes:", classes)

        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                print("json:", temp)

                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects dict if it's inside."""
        if obj:
            obj_key = f'{obj.__class__.__name__}.{obj.id}'
            del FileStorage.__objects[obj_key]
