from flask import Flask
from schedular.data.data_utils import get_all_blocks, get_all_students_from_pg, get_all_rotations_from_pg

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route("/")
def scheduler():
    blocks = get_all_blocks()
    print(type(blocks))
    return "works"


@app.route("/getSpreadsheet", methods=["GET"])
def export_spreadsheet():
    pass

