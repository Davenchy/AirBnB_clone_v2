#!/usr/bin/python3
"""Load all environment variables used to connect database"""

from os import environ

DB_USER = environ.get('HBNB_MYSQL_USER')
DB_PWD = environ.get('HBNB_MYSQL_PWD')
DB_HOST = environ.get('HBNB_MYSQL_HOST')
DB_NAME = environ.get('HBNB_MYSQL_DB')
HBNB_ENV = environ.get('HBNB_ENV')
DB_TYPE = environ.get('HBNB_TYPE_STORAGE')
