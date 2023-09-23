#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone."""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
import models
from models.base_model import Base
from models.utils.consts import HBNB_ENV, DB_USER, DB_PWD, DB_NAME, DB_HOST


class DBStorage:
    """This class manages storage of hbnb models in database format."""
    __engine = None
    __session = None

    def __init__(self):
        """Create the db engine."""

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                DB_USER, DB_PWD, DB_HOST, DB_NAME
            ), pool_pre_ping=True)

        if (HBNB_ENV == 'test'):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return the list of objects of (optional one type of) class."""
        if cls is None:
            classes = [models.classes[table] for table in models.tables]
            all_obj = {}
            for clsType in classes:
                query_result = self.__session.query(clsType).all()
                for obj in query_result:
                    all_obj[obj.objectKey] = obj
            return all_obj

        if (type(cls) == str):
            cls = models.classes[cls]

        result = self.__session.query(cls).all()
        return {obj.objectKey: obj for obj in result}

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
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        # to make Session thread-safe
        Scope = scoped_session(session_factory)
        self.__session = Scope()

    def close(self):
        """Closes storage"""
        self.__session.__class__.close(self.__session)
        self.reload()
        # if self.__session is Session and self.__session is not None:
        #     self.__session.close()
