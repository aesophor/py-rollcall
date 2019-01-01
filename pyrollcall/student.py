# -*- encoding: utf-8 -*-

import pyrollcall.utils as utils

class Student:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @property
    def has_photos(self):
        return len(utils.list_images(self.get_photo_dir())) > 0

    def get_photo_dir(self):
        return "faces/" + self.__str__() + "/"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not(self == other)

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'has_photos': self.has_photos
        }

    def __str__(self):
        return "_".join([self.id, self.name])
