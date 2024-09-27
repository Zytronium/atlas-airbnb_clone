#!/usr/bin/env python3
"""the FileStorage class."""
import json
import os



class FileStorage:
    """the FileStorage class"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """return the dictionary of all objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sdd a new object to the dictionary"""
        key = obj.id
        obj_name = obj.__class__.__name__
        FileStorage.__objects[f"{obj_name}.{key}"] = obj

    def save(self):
      """save the dict to the file"""
      dict = FileStorage.__objects.copy()
      with open(FileStorage.__file_path, 'w') as f:       
          

    def reload(self):
        """deserializes the file to __object"""
        if (os.path.isfile(FileStorage.__file_path)):
            