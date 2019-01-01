# -*- encoding: utf-8 -*-

class Session:
    """ Session records whether each student has arrived or not """
    def __init__(self, course):
        self.students_arrival = {}
        for s in course.students:
            self.students_arrival[s] = False

    def mark_arrived(student_id: str):
        """ Mark the specified student as arived
        :param student: The student who has just arrived
        """
        for student, arrived in self.students_arrival.items():
            if student.id == student_id:
                self.students_arrival[student] = True
