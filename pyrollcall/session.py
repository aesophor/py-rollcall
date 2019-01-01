# -*- encoding: utf-8 -*-

import pyrollcall.utils as utils

class Session:
    """ Session records whether each student has arrived or not """
    def __init__(self, course):
        self.course = course
        self.students_arrival = {}

        for s in course.students:
            self.students_arrival[s] = False

    def mark_arrived(self, student_id: str):
        """ Mark the specified student as arived
        :param student: The student who has just arrived
        """
        for student, arrived in self.students_arrival.items():
            if student.id == student_id:
                self.students_arrival[student] = True

    def export(self):
        """ Export the student arrival data to a log """
        timestamp = utils.get_datestamp()
        log_dir = "logs/{}".format(timestamp)
        utils.mkdir(log_dir)
        log_file = "{}/{}.txt".format(log_dir, self.course.name)

        print("[INFO] Exported log to {}".format(log_file))
        with open(log_file, 'w') as f:
            f.write(self.__str__())

    def __str__(self):
        arrived = sum([1 for s, arrived in self.students_arrival.items() if arrived])
        total = len(self.course.students)
        late = total - arrived
        late_student_names = [s.name for s, arrived in self.students_arrival.items() if not arrived]

        return "\r\n".join([
            "Course Name: " + self.course.name,
            "Export Time: " + utils.get_datetimestamp(),
            "Arrived: " + str(arrived) + " / Late: " + str(late) + " / Total: " + str(total),
            "Late Students: "]
        ) + "\r\n" + ",".join(late_student_names)
