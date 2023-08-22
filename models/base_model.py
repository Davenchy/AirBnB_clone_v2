#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from models import storage
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

            if 'created_at' not in kwargs:
                self.created_at = datetime.now()

            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        details = self.__dict__
        if '_sa_instance_state' in details:
            del details['_sa_instance_state']
        return '[{}] ({}) {}'.format(cls, self.id, details)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        storage.delete(self)

    @property
    def objectKey(self):
        """Returns the string representation of the instance

        Format: <class_name>.<uuid>

        Returns: string"""
        return BaseModel.generateObjectKey(self.__class__.__name__, self.id)

    @staticmethod
    def generateObjectKey(cls, id):
        """Returns the string representation of the instance

        Format: <class_name>.<uuid>

        Args:
            cls (str): class name
            id (str): instance id

        Returns: string"""
        return "{}.{}".format(cls, id)

    @classmethod
    def getRequiredAttributes(cls):
        """Returns a list of required attributes

        Returns: list"""
        table = getattr(cls, '__table__', None)
        if table is None:
            return []
        return [c.name for c in table.columns if (not c.primary_key
                                                  and not c.nullable
                                                  and not c.default)]
