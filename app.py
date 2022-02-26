from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import random
import csv

from helper import login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():

    data = []
    companies = []

    for i in range(5):
        data.append({
                "company": "Indeed",
                "jobType": "Intern",
                "pay": "1050",
                "jobSector": "Business",
                "description": "Shopee Academy takes pride in close partnership with all leaders, teams and individuals in Shopee to co-create learning solutions that work for them. We aim to become better versions of ourselves. Our comprehensive learning initiatives includes General, Functional and Leadership training to cater to different groups of employees."
                })
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

        tele_user = request.form.get("tele_user")
        user = request.form.get("username")
        Pass = request.form.get("password")

        list = [tele_user, user, Pass]


        with open("password.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(list)

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    username = ["admin"]
    password = {"admin" : "password"}

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