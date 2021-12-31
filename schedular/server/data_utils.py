"""
Functions for interacting with MySql
"""
import datetime
import os
import pymysql

from schedular.modules.rotation import Rotation
from schedular.modules.student import Student
from schedular.modules.block import Block

os.environ["SCHEDULAR_DB_HOST"] = "127.0.0.1"
os.environ["SCHEDULAR_DB_USER"] = "root"
os.environ["SCHEDULAR_DB_PASS"] = "password"
os.environ["SCHEDULAR_DB_NAME"] = "schedular"


def remove_newline(string):
    """
    remove annoyting newlines that get inserted into secrets
    :param string: String to remove newlines from
    :return: string without newlines
    """
    if isinstance(string, str):
        return string.replace("\n", "")
    return None


def none_to_zero(num):
    """
    :param num: if the parameter is none convert to 0
    :return: the number after checking if its none
    """
    if num is None:
        return 0
    return num


def mysql_connection():
    """
    get a connection to mysql
    """
    try_count = 0
    while try_count < 3:
        try:
            return pymysql.connect(host=remove_newline(os.getenv("SCHEDULAR_DB_HOST")),
                                   user=remove_newline(os.getenv("SCHEDULAR_DB_USER")),
                                   password=remove_newline(os.getenv("SCHEDULAR_DB_PASS")),
                                   database=remove_newline(os.getenv("SCHEDULAR_DB_NAME")),
                                   port=3306,
                                   cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError:
            try_count += 1
            if try_count == 3:
                raise


def execute_sql(sql, parameter, select=True):
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parameter)
                if select:
                    return cursor.fetchall()
                connection.commit()
                return None
    except pymysql.err.OperationalError:
        return "problem connection with mysql"


def get_all_students():
    students_sql = f"""SELECT * FROM students"""
    students = execute_sql(students_sql, None, True)

    return students


def get_all_students_from_pg(pg_year):
    students_sql = f"""SELECT * FROM students WHERE PG_YEAR = '{pg_year}'"""
    students = execute_sql(students_sql, None, True)

    return students


def get_all_rotations_from_pg(pg_year):
    rotations_sql = f"""SELECT * FROM rotations WHERE PG_YEAR = '{pg_year}' Order by compliance DESC"""
    rotations = execute_sql(rotations_sql, None, True)
    return rotations


def get_all_blocks():
    blocks_sql = f"""SELECT * FROM blocks"""
    blocks = execute_sql(blocks_sql, None, True)

    return blocks


def add_total_compliance(rotations):
    compliance = 0
    for rotation in rotations:
        compliance += rotation["Compliance"]
    return compliance


def create_schedule_student(student, pg_year):
    """
    :param student:
    :param pg_year:
    :return:
    """

    student = Student(student)
    full_name = student.first_name + ", " + student.last_name
    rotations = get_all_rotations_from_pg("PYG1-CORE")
    block = 1
    compliance = add_total_compliance(rotations)
    stud_schedule = []
    schedule = {full_name: stud_schedule}

    while compliance > 0:
        for rotation in rotations:
            if rotation["Compliance"] > 0:
                cur_rotation = {"Block": block, "Rotation": rotation["Rotation_Name"]}
                block += 1
                compliance -= 1
                rotation["Compliance"] -= 1
                stud_schedule.append(cur_rotation)
    return schedule


def create_pg_schedule():
    students = get_all_students_from_pg("PYG1-CORE")
    pg_schedule = []
    for s in students:
        cur_stud = create_schedule_student(s, "PYG1-CORE")
        pg_schedule.append(cur_stud)

    print(pg_schedule)
