# -*- encoding: utf-8 -*-

class Student:
    """ Student """
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @property
    def photo_dir(self):
        return "faces/" + self.__str__() + "/"

    def __equ__(self, other):
        if isinstance(other, Student):
            return self.id == other.id
        return False

    def __str__(self):
        return "_".join([self.id, self.name])
