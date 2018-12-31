# -*- encoding: utf-8 -*-

from pyrollcall.database import Database
from pyrollcall.course import Course
from pyrollcall.student import Student
import pyrollcall.face as face

faces_dir = "faces/"

def main():
    # Try to unpickle database from file.
    try:
        db = Database("rollcall.db")
        db.load()
    except FileNotFoundError:
        print("[WARNING] Database file not found. Creating a new one...")

    c = Course(1071, "Image Processing")
    s = Student("U10516045", "Marco")
    c.add_student([s])

    db = Database("rollcall.db")
    db.courses.append(c)
    db.dump()

    face.encode_faces(db, faces_dir)
    name = face.recognize_face(db, "/home/aesophor/Code/py-rollcall/test/Marco0.png")
    print(name)
