"""
Functions for interacting with MySql
"""
import datetime
import os
import pymysql
from schedular.modules.rotation import Rotation
from schedular.modules.student import Student
from schedular.modules.block import Block


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
                                   cursorclass=pymysql.cursors.DictCursor,
                                   client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)
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
    students_sql = f"""SELECT * FROM students WHERE grad_year = '{pg_year}'"""
    students = execute_sql(students_sql, None, True)

    return students


def insert_new_student(new_student):
    """
    Adds new student to data base
    :param new_student: dict of new student added from form
    :return: the newly added student id
    """
    sql = f"""INSERT INTO students (first_name, last_name, phone_number, military_branch, dept_of_def_id, grad_year) 
    VALUES(%s, %s, %s, %s, %s, %s)"""
    values = []
    for field in new_student:
        if new_student[field] == '':
            new_student[field] = None
        values.append(new_student[field])

    return execute_sql(sql, tuple(values), False)


def insert_new_rotation(new_rotation):
    """
    Adds new student to data base
    :param new_rotation: dict of new rotation added py PG_YEAR
    :return: the newly added student id
    """
    sql = f"""INSERT INTO rotations (Rotation_Name, Can_Leave, On_Call, On_Site, Compliance, PG_YEAR) 
    VALUES(%s, %s, %s, %s, %s, %s)"""
    values = []
    for field in new_rotation:
        if new_rotation[field] == '':
            new_rotation[field] = None
        values.append(new_rotation[field])

    return execute_sql(sql, tuple(values), False)


def get_all_rotations_from_pg(pg_year):
    rotations_sql = f"""SELECT * FROM rotations WHERE PG_YEAR = '{pg_year}' Order by compliance DESC"""
    rotations = execute_sql(rotations_sql, None, True)
    return rotations


def get_all_rotations():
    rotations_sql = f"""SELECT * FROM rotations"""
    rotations = execute_sql(rotations_sql, None, True)
    return rotations


def get_all_blocks():
    """
    SQL script to return list of block objects
    :return:
    """
    blocks_sql = f"""SELECT * FROM blocks"""
    blocks = execute_sql(blocks_sql, None, True)

    return blocks


def get_block_info_rows():
    blocks = get_all_blocks()
    row_blk = ["Block"]
    row_blk_start = ["Start"]
    row_blk_end = ["End"]
    row_blk_wrk_days_hol = ["Workdays(hol)"]
    row_blk_wrk_days = ["Workdays"]
    days = ["Days"]

    for block in blocks:
        row_blk.append(block["Block_Id"])
        row_blk_start.append(block["Start_Date"])
        row_blk_end.append(block["End_Date"])
        row_blk_wrk_days_hol.append(block["Work_Days_hol"])
        row_blk_wrk_days.append(block["Work_Days"])
        days.append(block["Days"])

    rows = [tuple(row_blk), tuple(row_blk_start), tuple(row_blk_end), tuple(row_blk_wrk_days_hol),
            tuple(row_blk_wrk_days), tuple(days)]
    return rows


def add_total_compliance(rotations):
    compliance = 0
    for rotation in rotations:
        compliance += rotation["Compliance"]
    return compliance


def create_schedule_student(student):
    """
    :param student:
    :return:
    """
    student = Student(student).get_student()
    full_name = student['first_name'] + ", " + student['last_name']
    rotations = get_all_rotations_from_pg(student["grad_year"])
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


def create_schedule_for_pg_year(pg_year):
    """
    Creates a rotations schedule for all students in a same PG_Year
    :param pg_year: Year that rotation schedule needs creation for
    :return: List of student dicts ie [{student:[rotations]},....]
    """
    students = get_all_students_from_pg(pg_year)
    pg_schedule = []
    for s in students:
        cur_stud = create_schedule_student(s)
        pg_schedule.append(cur_stud)

    return pg_schedule

def get_all_block_years():
    sql = f"""Select distinct(block_sched_year) from blocks"""
    all_blocks = execute_sql(sql, None, True)
    print(all_blocks)
    return all_blocks


