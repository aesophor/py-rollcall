# -*- encoding: utf-8 -*-

from pyrollcall.student import Student

class Course:
    def __init__(self, year: str, name: str):
        self.year = year
        self.name = name
        self.students = []

    def add_student(self, students: list):
        self.students += students

    def remove_student(self, s: Student):
        self.students.remove(s)

    def __hash__(self):
        return hash((self.year, self.name))

    def __eq__(self, other):
        if isinstance(other, Course):
            return (self.year == other.year) and (self.name == other.name)
        return False

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return "_".join([self.year, self.name])
