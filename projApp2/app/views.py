from app import app
from flask import render_template
from flask import request, redirect, url_for
import os
import remove_sp_character
#import ourFileName
import time
from flask import abort
from werkzeug.utils import secure_filename
#app.config["SCHEMA_UPLOADS"] = "/home/sam/venv_final/app/static/schema" #alter
app.config["SCHEMA_UPLOADS"] = "/Users/Shivani T Eswara/finyear/visionapi/projApp2/app/static/schema"
#app.config["ANSWER_UPLOADS"] = "/home/sam/venv_final/app/static/answers" #alter
app.config["ANSWER_UPLOADS"] = "/Users/Shivani T Eswara/finyear/visionapi/projApp2/app/static/answers"

app.config["ALLOWED_FILE_EXTENSIONS"] = ["TXT","DOC","PDF","JPEG","JPG","PNG"]
# subject = ""
# inputType = ""
@app.route("/")
def index():
    if(True):
        return redirect(url_for('uploadFiles'))
    else:
        return "<h1>SORRY! THERE SEEMS TO BE AN ISSUE.</h1>"

@app.route("/results",methods=['POST'])
def results():
    if request.method == "POST":
        if request.files:
            answer = request.files["answer"]
            schema = request.files["schema"]
            subject = request.form["subject-select"]
            inputType = request.form["input-select"]
            print("yayyyyy!!",subject,inputType)
            if answer.filename == "" or schema.filename == "":
                print("No filename")
                return redirect(url_for('uploadFiles'))

            if allowed_files(answer.filename) and allowed_files(schema.filename):
                answer_file = secure_filename(answer.filename)
                answer.save(os.path.join(app.config["ANSWER_UPLOADS"], answer_file))
                #answer_path=os.path.join(app.config["ANSWER_UPLOADS"], filename)
                print("Answer file : "+answer_file)
                schema_file = secure_filename(schema.filename)
                schema.save(os.path.join(app.config["SCHEMA_UPLOADS"], schema_file))
                #schema_path=os.path.join(app.config["SCHEMA_UPLOADS"], filename)
                print("Schema file : "+schema_file)
                print("Files saved")
                # redirect(url_for('results',subject=subject,inputType=inputType))

            else:
                print("That file extension is not allowed")
                return redirect(url_for('uploadFiles'))
            

    print("subject------------",subject)
    result = remove_sp_character.receive_file(subject,inputType,answer_file,schema_file)
    # resp = ourFileName.ourFunctionName(True)
    # return redirect(url_for('result',subject=subject))
    #time.sleep(15) #for letting vision API process
    print(result)
    return render_template("result.html",foobar=result)
def allowed_files(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/uploadFiles", methods=["GET", "POST"])
def uploadFiles():
    return render_template("uploadFiles.html")