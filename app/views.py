from app import app
from flask import render_template
from flask import request, redirect
import os
from flask import abort
from werkzeug.utils import secure_filename
app.config["SCHEMA_UPLOADS"] = "/home/sam/venv_final/app/static/schema"
app.config["ANSWER_UPLOADS"] = "/home/sam/venv_final/app/static/answers"

app.config["ALLOWED_FILE_EXTENSIONS"] = ["TXT","DOC","PDF"]

@app.route("/")
def index():
    return "Hi there! loremIpsum"

@app.route("/result")
def about():
    return render_template("result.html")

# @app.route("/uploadFiles", methods=["GET", "POST"])
# def upload_files():
#     if request.method == "POST":
#         if request.files:
#             schema = request.files["schema"]
#             print(schema)
#             answer = request.files["answer"]
#             print(answer)

#             return redirect(request.url)


#     return render_template("uploadFiles.html")


def allowed_files(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/uploadFiles", methods=["GET", "POST"])
def upload_files():

    if request.method == "POST":
        if request.files:
            answer = request.files["answer"]
            schema = request.files["schema"]
            if answer.filename == "" or schema.filename=="":
                print("No filename")
                return redirect(request.url)

            if allowed_files(answer.filename) and allowed_files(schema.filename):
                filename = secure_filename(answer.filename)
                answer.save(os.path.join(app.config["ANSWER_UPLOADS"], filename))
                filename = secure_filename(schema.filename)
                schema.save(os.path.join(app.config["SCHEMA_UPLOADS"], filename))
                print("Files saved")
                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("uploadFiles.html")

    

