# -*- encoding: utf-8 -*-

from pyrollcall.student import Student

class Course:
    def __init__(self, year: int, name: str):
        self.year = year
        self.name = name
        self.students = []

    def add_student(self, students: list):
        self.students += students

    def remove_student(self, s: Student):
        self.students.remove(s)
