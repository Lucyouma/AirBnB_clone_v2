#!/usr/bin/python3
"""
Defines the DBStorage class
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Dictionary to map class names to their respective classes
class_mapping = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class DBStorage:
    """Handles interactions with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance"""
        db_user = getenv("HBNB_MYSQL_USER")
        db_password = getenv("HBNB_MYSQL_PWD")
        db_host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")
        db_env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            f"mysql+mysqldb://{db_user}:{db_password}@{db_host}/{db_name}"
        )

        if db_env == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects of
        a given class, or all classes
        """
        result = {}
        for class_name in class_mapping:
            if cls is None or cls is class_mapping[class_name] \
                    or cls == class_name:
                objects = self.__session.query(class_mapping[class_name]).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    result[key] = obj
        return result

    def new(self, obj):
        """Adds a new object to the current session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Removes an object from the current session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the session"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieves a specific object by class
        and ID, or returns None if not found
        """
        if cls not in class_mapping.values():
            return None
        all_objects = models.storage.all(cls)
        for obj in all_objects.values():
            if obj.id == id:
                return obj
        return None

    def count(self, cls=None):
        """Counts the number of objects in
        storage for a given class, or all classes
        """
        total = 0
        if cls is None:
            for class_type in class_mapping.values():
                total += len(models.storage.all(class_type))
        else:
            total = len(models.storage.all(cls))
        return total
