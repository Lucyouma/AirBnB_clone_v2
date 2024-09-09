#!/usr/bin/python3
"""Module defining a class to manage file storage for the hbnb clone"""
import json
import models
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


class FileStorage:
    """Handles storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects currently in storage"""
        if cls is None:
            return self.__objects
            # object_dict = {}
        else:
            object_dict = {}
            # return {k: v for k, v in self.__objects.items()
            # if isinstance(v, cls) or cls == v.__class__.__name__}
            for k, v in self.__objects.items():
                if cls == v.__class__ or cls == v.__class__.__name__:
                    object_dict[k] = v
            return object_dict

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        key = f"{obj.to_dict()['__class__']}.{obj.id}"
        # self.all()[key] = obj
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Serializes the storage dictionary to a file"""
        with open(self.__file_path, "w") as f:
            temp = {key: val.to_dict() for key, val in self.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Deserializes the storage dictionary from a file"""

        try:
            with open(self.__file_path, "r") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Removes an object from the current session"""
        if obj:
            object_key = obj.__class__.__name__ + '.' + obj.id
            if object_key in self.__objects:
                del self.__objects[object_key]

    def close(self):
        """
        deserialize json objects
        """
        self.reload()

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
                total += len(models.storage.all(class_type).values())
        else:
            total = len(models.storage.all(cls).values())
        return total
