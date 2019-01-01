# -*- encoding: utf-8 -*-

from imutils import paths
import face_recognition
import pickle

from pyrollcall.course import Course
from pyrollcall.student import Student

class Database:
    def __init__(self, db_file_path: str):
        self.db_file_path = db_file_path
        self.courses = []
        self.students = []
        self.face_encodings = []

    def load(self):
        """ Unpickle courses and students from the file """
        with open(self.db_file_path, 'rb') as f:
            data = pickle.load(f)
            self.courses = data["courses"]
            self.students = data["students"]

    def dump(self):
        """ Pickle courses and students to the file """
        with open(self.db_file_path, 'wb') as f:
            data = pickle.dump({
                "courses": self.courses,
                "students": self.students
            }, f)


    def add_course(self, year: str, name: str):
        """ Add a new course 
        :param year: The year of the course
        :param name: The name of the course
        :return: The course we've just created
        """
        id = 0 if len(self.courses) == 0 else self.courses[len(self.courses) - 1].id + 1
        course = Course(id, year, name)
        self.courses.append(course)
        return course

    def get_course(self, id: int):
        """ Get an existing course
        :param id: The id of the course
        :return: Course if found, None if not found
        """
        for c in self.courses:
            if c.id == id:
                return c
        return None

    def remove_course(self, course):
        """ Remove the specified course
        :param course: The course to remove
        """
        if course in self.courses:
            self.courses.remove(course)


    def add_student(self, id: str, name: str):
        """ Add a new student
        :param id: The id of the student
        :param name: The name of the student
        :return: The student we've just created
        """
        student = Student(id, name)
        self.students.append(student)
        return student

    def get_student(self, id: str):
        """ Get an existing student
        :param id: The id of the student
        :return: Student if found, None if not found
        """
        for s in self.students:
            if s.id == id:
                return s
        return None

    def remove_student(self, student):
        """ Remove the specified student. It also removes all occurrences
        of this student from all existing courses.
        :param student: The student to remove
        """
        if student in self.students:
            for course in self.courses:
                if student in course.students:
                    course.students.remove(student)
            self.students.remove(student)
