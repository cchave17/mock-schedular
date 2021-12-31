from flask import Flask, render_template, url_for, request
from schedular.server.data_utils import get_all_students

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route("/")
def scheduler():
    students = get_all_students()
    headings = ("first name", "last name", "PG Year")
    rows = []
    for s in students:
        row = (s["first_name"], s["last_name"], s["grad_year"])
        rows.append(row)
    rows = tuple(rows)
    return render_template('index.html', s_headings=headings, sudents=rows)


@app.route("/new_student", methods=["GET", "POST"])
def get_new_student_page():
    if request.method == "POST":
        data = request.form.to_dict()
        return render_template('index.html')
    return render_template('new_student.html')


@app.route("/index", methods=["GET"])
def return_home():
    pass