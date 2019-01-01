# -*- encoding: utf-8 -*-

import pyrollcall.utils as utils

class Session:
    """ Session records whether each student has arrived or not """
    def __init__(self, course):
        self.course = course
        self.students_arrival = {}
        
        self.total = len(self.course.students)
        self.arrived = 0
        self.unpresent = self.total

        for s in course.students:
            self.students_arrival[s] = False

    @property
    def unpresent_students(self):
        return [s.name for s, arrived in self.students_arrival.items() if not arrived]

    def mark_as_arrived(self, student_id: str):
        """ Mark the specified student as arived
        :param student: The student who has just arrived
        """
        for student, arrived in self.students_arrival.items():
            if student.id == student_id:
                self.students_arrival[student] = True
                self.arrived += 1
                self.unpresent -= 1
    
    def export(self):
        """ Export the student arrival data to a log """
        timestamp = utils.get_datestamp()
        late_student_names = self.unpresent_students
        log_dir = "logs/{}".format(timestamp)
        utils.mkdir(log_dir)

        log_file = "{}/{}.txt".format(log_dir, self.course.name)

        log_content = "\r\n".join([
            "Course Name: " + self.course.name,
            "Export Time: " + utils.get_datetimestamp(),
            "Arrived: " + str(self.arrived) + " / Late: " + str(self.unpresent) + " / Total: " + str(self.total),
            "Late Students: "]
        ) + "\r\n" + ",".join(late_student_names)

        with open(log_file, 'w') as f:
            f.write(log_content)

        print("[INFO] Exported log to {}".format(log_file))

    def __str__(self):
        return "({}) {} - Arrival Rate: {}/{}".format(
            self.course.semester, self.course.name, self.arrived, self.total)
