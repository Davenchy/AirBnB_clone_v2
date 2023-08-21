#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone."""
from sqlalchemy import create_engine
from os import environ
from sqlalchemy.orm import sessionmaker, scoped_session
import models


class DBStorage:
    """This class manages storage of hbnb models in database format."""
    __engine = None
    __session = None

    def __init__(self):
        """Create the db engine."""

        user = environ.get('HBNB_MYSQL_USER')
        passwd = environ.get('HBNB_MYSQL_PWD')
        host = environ.get('HBNB_MYSQL_HOST')
        db = environ.get('HBNB_MYSQL_DB')

        self.__engine = create_engine(f'mysql+mysqldb://{user}:{passwd}\
                                           @{host}/{db}', pool_pre_ping=True)

        if (environ.get('HBNB_ENV') == 'test'):
            Base = models.general_injector['Base']
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return the list of objects of (optional one type of) class."""
        if not cls:
            classes = models.injector.classes.values()
            all_obj = {}
            for iclass in classes:
                query_result = self.__session.query(iclass).all()
                for obj in query_result:
                    all_obj[f'{iclass.__name__}.{obj.id}'] = obj
            return all_obj

        if (type(cls) == str):
            cls = eval(cls)
        cls_objects = {}
        query_result = self.__session.query(cls).all()
        for obj in query_result:
            cls_objects[f'{cls.__name__}.{obj.id}'] = obj
        return cls_objects

    def new(self, obj):
        """Adds new object to storage dictionary."""
        self.__session.add(obj)

    def save(self):
        """Saves storage dictionary to db."""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from the current database session if exists."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base = models.general_injector['Base']
        Base.metadata.create_all(DBStorage.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        # to make Session thread-safe
        Session = scoped_session(session_factory)
        self.__session = Session()
