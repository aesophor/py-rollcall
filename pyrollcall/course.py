# -*- encoding: utf-8 -*-

from pyrollcall.student import Student

class Course:
    def __init__(self, id: int, year: str, name: str):
        self.id = id
        self.year = year
        self.name = name
        self.students = []

    def add_students(self, students: list):
        self.students += students

    def add_student(self, s: Student):
        if s not in self.students:
            self.students.append(s)

    def remove_student(self, s: Student):
        if s in self.students:
            self.students.remove(s)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return "_".join([self.year, self.name])
