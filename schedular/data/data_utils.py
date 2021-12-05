"""
Functions for interacting with MySql
"""
import datetime
import os
import pymysql

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


def get_all_students_from_PG():
    # sql = f"""SELECT * FROM students WHERE PG_YEAR = '{year}'"""
    sql = f"""SELECT * FROM students"""
    students = execute_sql(sql, None, True)
    for student in students:
        full_name = student['first_name'] + ", " + student['last_name']
        print(full_name)


get_all_students_from_PG()
