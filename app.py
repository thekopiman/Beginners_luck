from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import random
import csv

from helper import login_required

from web_firebaseDB import WebFireBaseDB
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)

cred = credentials.Certificate(r"C:\Users\agohs\Downloads\inteetsgintern-firebase-adminsdk-bh9du-abb3ea5cbb.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://inteetsgintern-default-rtdb.asia-southeast1.firebasedatabase.app"})

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():

    def getJobs():
        getJob = db.reference('jobs/')
        jobData = getJob.get()
        return jobData

    data = list(getJobs().values())
    companies = []
    
    for i in range(20):
        companies.append("Google")

    return render_template("index.html", data=data, companies=companies)


@app.route("/profile")
@login_required
def profile():

    return render_template("profile.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # (Optional) Set to telegram_username
        tele_user = request.form.get("tele_user")
        user = request.form.get("username")
        Pass = request.form.get("password")
        # Add this into the register page
        full_name = request.form.get("full_name")
        # Add this into the register page
        education_cert = request.form.get("education_cert")

        list = [tele_user, user, Pass]

        hello = WebFireBaseDB()
        # If this condition is true, that means that REGISTER should yield error
        if hello.check_exisiting_user(user):
            raise Exception  # Instead of raise error, please go back to the login screen and inform the user that the username has been used
        else:
            hello.register_account(user, Pass, full_name,
                                   education_cert, tele_user)

        # with open("password.csv", "a", newline="") as file:
        #     writer = csv.writer(file)
        #     writer.writerow(list)

        firebase_admin.delete_app(firebase_admin.get_app())

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    hello = WebFireBaseDB()
    session.clear()

    username = list(hello.get_login_details().keys())
    password = hello.get_login_details().keys()

    firebase_admin.delete_app(firebase_admin.get_app())

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return print("must provide username")
        else:
            user = request.form.get("username")
            print(user)

        # Ensure password was submitted
        if not request.form.get("password"):
            return print("must provide password")
        else:
            Pass = request.form.get("password")
            print(Pass)

        # Query database for username
        # rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #    return print("invalid username and/or password")
        if user not in username:
            return print("Invalid user or pass")
        if Pass != password[user]:
            return print("Invalid user or pass")

        session["user"] = random.randint(0, 9)

        return redirect("/")
    else:
        return render_template("/login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
