#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""
        cities = ""

    def __init__(self, *args, **kwargs):
        """
        state initialization
        """
        super().__init__(self, *args, **kwargs)

    @property
    def cities(self):
        """
        Retrieve cities from file storage
        """
        all_cities = models.storage.all("City")
        cities = []
        for city in all_cities.values():
            if city.state_id == self.id:
                cities.append(city)
        return cities
