# -*- encoding: utf-8 -*-

from imutils import paths
import face_recognition
import pickle

from pyrollcall.course import Course
from pyrollcall.face import FaceEncoding

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
