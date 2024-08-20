#!/usr/bin/python3
"""Module defining a class to manage file storage for the hbnb clone"""
import json


class FileStorage:
    """Handles storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns a dictionary of all objects currently in storage"""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        key = f"{obj.to_dict()['__class__']}.{obj.id}"
        self.all()[key] = obj

    def save(self):
        """Serializes the storage dictionary to a file"""
        with open(self.__file_path, "w") as f:
            temp = {key: val.to_dict() for key, val in self.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Deserializes the storage dictionary from a file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }

        try:
            with open(self.__file_path, "r") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """
        deserialize json objects
        """
        self.reload()
