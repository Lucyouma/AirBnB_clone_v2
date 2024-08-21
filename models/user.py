#!/usr/bin/python3
"""Defines the User class for the HBNB project."""

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Represents a user of the application."""

    __tablename__ = 'users' if models.storage_t == 'db' else None

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a new user instance."""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Encrypts the password before setting it."""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
