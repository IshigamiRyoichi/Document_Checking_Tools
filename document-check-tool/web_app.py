from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pyrebase
import json, os
from werkzeug.utils import secure_filename
import subprocess
import re

with open("./static/json/firebase.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

allowed_extenstions = set(["pdf"])

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
UPLOADS_FOLDER = "./uploads/"
app.config["UPLOAD_FOLDER"] = UPLOADS_FOLDER

def allwed_file(filename):
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extenstions

def upload_pdf_file(pdf_file):
    print("ccc")
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], "target.pdf")
    print(file_path)
    pdf_file.save(file_path)

def run_pdf2text():
    cmd = "pdftotext ./uploads/target.pdf ./uploads/target.md"
    subprocess.run(cmd, shell=True, capture_output=True, text=True)

def run_textlint_and_get_result_list():
    cmd = "npx textlint ./uploads/target.md"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # print("--------")
    result_list = result.stdout.split("\n")
    result_table = []
    for result in result_list[2:-4]:
        tmp_result = result.split(" error ")
        if len(tmp_result) >= 2:
            row = tmp_result[0].split(":")[0].strip()
            colum = tmp_result[0].split(":")[1].strip()
            error_data = re.sub("ja-technical-writing/[a-z | -]*","",tmp_result[1]).strip()
            result_table.append([row,colum,error_data])
    # print(result_table)
    return result_table

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", msg="")
    
    email = request.form["email"]
    password = request.form["password"]
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # print(user)
        session["usr"] = email
        return redirect(url_for("index"))
    except:
        print("ログイン失敗")
        return render_template("login.html", msg="メールアドレスまたは，パスワードが間違ってます")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():    
    if request.method == "GET":
        return render_template("create_account.html", msg="")
    email = request.form["email"]
    password = request.form["password"]
    try:
        user = auth.create_user_with_email_and_password(email, password)
        session["usr"] = email
        return redirect(url_for("index"))
    except:
        print("アカウント作成できませんでした")
        return render_template("login.html", msg="アカウント作成出来ませんでした")
    
@app.route("/index", methods=["GET"])
def index():
    usr = session.get("usr")
    if usr == None:
        return redirect(url_for("login"))
    return render_template("index.html", usr=usr)

@app.route("/", methods=["GET"])
def root():
    usr = session.get("usr")
    if usr == None:
        return redirect(url_for("login"))
    return redirect(url_for("index"))

@app.route("/result", methods=["GET", "POST"])
def resulr():
    usr = session.get('usr')
    if usr == None:
        return redirect(url_for('login'))
    elif request.method == "POST":
        pdf_file = request.files["pdf_file"]
        upload_pdf_file(pdf_file)
        run_pdf2text()
        result_table = run_textlint_and_get_result_list()
        return render_template("result.html", result_table=result_table)
    return redirect(url_for('index'))
@app.route('/logout')
def logout():
    del session['usr']
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)