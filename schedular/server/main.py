from flask import Flask, render_template, url_for, request, redirect
from schedular.server.sql_utils import get_all_students, insert_new_student, get_all_rotations, \
    insert_new_rotation, create_schedule_for_pg_year, get_block_info_rows, get_all_block_years

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route("/")
def scheduler():
    students = get_all_students()
    student_headings = ("first name", "last name", "PG Year")
    student_rows = []
    for s in students:
        row = (s["first_name"], s["last_name"], s["grad_year"])
        student_rows.append(row)
    student_rows = tuple(student_rows)

    rotations = get_all_rotations()
    rotation_headings = ("Rotation_Name", "Can_Leave", "On_Call", "On_Site", "Compliance", "PG_YEAR")
    rotation_rows = []
    for r in rotations:
        row = (r["Rotation_Name"], r["Can_Leave"], r["On_Call"], r["On_Site"],
               r["Compliance"], r["PG_YEAR"])
        rotation_rows.append(row)
    rotation_rows = tuple(rotation_rows)

    # blocks_dict = get_all_block_years()
    # print("block_dicts: ",blocks_dict)
    # block_years = []
    #
    # for b in blocks_dict:
    #     block_years.append(b.get('block_sched_year'))
    #
    # block_year = tuple(block_years)

    return render_template('index.html', s_headings=student_headings, sudents=student_rows,
                           r_headings=rotation_headings, rotations=rotation_rows)


@app.route("/new_student", methods=["GET", "POST"])
def add_new_student():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
        insert_new_student(data)
        return redirect(url_for('scheduler'))
    return render_template('new_student.html')


@app.route("/new_rotation", methods=["GET", "POST"])
def add_new_rotation():
    if request.method == "POST":
        data = request.form.to_dict()
        insert_new_rotation(data)
        return redirect(url_for('scheduler'))
    return render_template('new_rotation.html')


@app.route("/render_schedule", methods=["GET"])
def generate_schedule():
    # Change parameter from PYG1-CORE to a variable
    data = create_schedule_for_pg_year("PYG1-CORE")
    rows = get_block_info_rows()

    for s in data:
        name = next(iter(s))
        row_stud_schedule = [name]
        for sched in s[name]:
            row_stud_schedule.append(sched["Rotation"])
        rows.append(tuple(row_stud_schedule))
    rows = tuple(rows)
    return render_template('render_schedule.html', rows=rows)


@app.route("/create_block_schedule", methods=["GET","POST"])
def create_block_schedule():
    if request.method == "POST":
        print(request.form.to_dict())
    return render_template('create_block_schedule.html')

