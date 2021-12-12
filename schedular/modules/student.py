"""
Module for studnet object
"""


class Student:
    """
    Class for Student
    """

    def __init__(self, fields):
        """
        :param fields:
        """
        self.student_id = fields.get("student_id")
        self.first_name = fields.get("first_name")
        self.last_name = fields.get("last_name")
        self.pg_year = fields.get("PG_YEAR")

    def get_student(self):
        student = {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "PG_YEAR": self.pg_year
        }
        return student
