#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import sqlalchemy
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

time = '%Y-%m-%dT%H:%M:%S.%f'

try:
    from models import storage_t
    if storage_t == "db":
        Base = declarative_base()
    else:
        Base = object
except ImportError:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if 'Base' in globals() and issubclass(Base, object):
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.now)
        updated_at = Column(DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # storage.new(self)
        else:
            self.id = str(uuid.uuid4())

            if 'created_at' in kwargs:
                try:
                    self.created_at = datetime.strptime(kwargs['created_at'],
                                                        time)
                except Exception as e:
                    print("invalid date format for created at")
            else:
                self.created_at = datetime.now()
            if 'updated_at' in kwargs:
                try:
                    self.updated_at = datetime.strptime(kwargs['updated_at'],
                                                        time)
                except Exception as e:
                    print("Invalid date format for updated_at")
            else:
                self.updated_at = datetime.now()

            if '__class__' in kwargs:
                del kwargs['__class__']

            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        if isinstance(self.created_at, datetime):
            dictionary['created_at'] = self.created_at.isoformat()
        else:
            dictionary['created_at'] = str(self.created_at)
        if isinstance(self.updated_at, datetime):
            dictionary['updated_at'] = self.updated_at.isoformat()
        else:
            dictionary['updated_at'] = str(self.updated_at)

        if '_sa_instance_state' in dictionary:
            dictionary.pop('_sa_instance_state')

        return dictionary

    def delete(self):
        """
        DELETES instance from storage
        """
        from models import storage
        storage.delete(self)
