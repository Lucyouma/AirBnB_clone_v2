#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import Base, BaseModel
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from os import getenv


class State(Base, BaseModel):
    """ State class """
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """
            Retrieve cities from file storage
            """
            return [city for city in models.storage.all('City').values()
                    if city.state_id == self.id]
