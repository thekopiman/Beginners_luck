from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import random

from helper import login_required

from web_firebaseDB import WebFireBaseDB
import firebase_admin
from database import Backend

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():

   hello = Backend()
   data = list(hello.getData().values())
   companies = []
   firebase_admin.delete_app(firebase_admin.get_app())
   companies = []
   welcome = "Welcome Kurt"
   
    
   for i in range(20):
       companies.append("Google")

   return render_template("index.html", data=data, companies=companies, welcome=welcome)

@app.route("/upload")
@login_required
def upload():

    if request.method == "POST":
        job_type = request.form.get("job_type")
        requirement = request.form.get("requirement")
        job_sector = request.form.get("job_sector")
        pay = request.form.get("pay")
        desc = request.form.get("desc")

        return redirect ("/")
    else:
        return render_template("upload.html")

@app.route("/profile")
@login_required
def profile():
   
   return render_template("profile.html")


@app.route("/home")
def home():

    return render_template("home.html")

@app.route("/emp_reg", methods=["GET", "POST"])
def emp_reg():

    field_error = "*All fields must be filled."

    if request.method == "POST":

        # (Optional) Set to telegram_username
        company_name = request.form.get("company_name")
        user = request.form.get("username")
        Pass = request.form.get("password")

        if not user or not Pass or not company_name:
            return render_template("emp_reg.html", field_error=field_error)
        
        return render_template("login.html")
    else:
        return render_template("emp_reg.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    
    field_error = "*All fields must be filled."
    user_error = "Username has already been taken"

    if request.method == "POST":

        # (Optional) Set to telegram_username
        tele_user = request.form.get("tele_user")
        user = request.form.get("username")
        Pass = request.form.get("password")
        # Add this into the register page
        full_name = request.form.get("full_name")
        # Add this into the register page
        education_cert = request.form.get("education_cert")

        if not user or not Pass or not full_name or not education_cert:
            return render_template("register.html", field_error=field_error)

        # list = [tele_user, user, Pass]

        hello = WebFireBaseDB()
        # If this condition is true, that means that REGISTER should yield error
        if hello.check_exisiting_user(user):
            return render_template("register.html", user_error=user_error)  # Instead of raise error, please go back to the login screen and inform the user that the username has been used
        else:
            hello.register_account(user, Pass, full_name,
                                   education_cert, tele_user)

        # with open("password.csv", "a", newline="") as file:
        #     writer = csv.writer(file)
        #     writer.writerow(list)

        firebase_admin.delete_app(firebase_admin.get_app())

        return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    hello = WebFireBaseDB()
    session.clear()

    username = list(hello.get_login_details().keys())
    password = hello.get_login_details()

    field_error = "*All fields must be filled."
    userpass_error = "*Username/password is invalid."

    firebase_admin.delete_app(firebase_admin.get_app())

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            print("must provide username")
            return render_template("login.html", field_error=field_error)
        else:
            user = request.form.get("username")

        # Ensure password was submitted
        if not request.form.get("password"):
            print("must provide password")
            return render_template("login.html", field_error=field_error)
        else:
            Pass = request.form.get("password")

        # Query database for username
        # rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #    return print("invalid username and/or password")
        if user not in username:
            print("Invalid user or pass")
            return render_template("login.html", userpass_error=userpass_error)
        if Pass != password[user]:
            print("Invalid user or pass")
            return render_template("login.html", userpass_error=userpass_error)

        session["user"] = random.randint(0, 9)

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
