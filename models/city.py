#!/usr/bin/python3
'''
    Define the class City.
'''
import models
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    '''
        Define the class City that inherits from BaseModel.
        '''

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="all, delete, delete-orphan")
    else:
        state_id = ""
        name = ""
        places = ""

    def __init__(self, *args, **kwargs):
        """
        state initialization
        """
        super().__init__(*args, **kwargs)
