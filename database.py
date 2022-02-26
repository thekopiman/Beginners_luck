from random import randint
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from uuid import uuid4
import json


class Backend:
    def __init__(self):
        cred = credentials.Certificate(
            r"C:\Users\agohs\Downloads\inteetsgintern-firebase-adminsdk-bh9du-abb3ea5cbb.json")
        firebase_admin.initialize_app(
            cred, {"databaseURL": "https://inteetsgintern-default-rtdb.asia-southeast1.firebasedatabase.app"})

        gradeMap = ["degree", "diploma", "A level", "O level", "N level"]

        self.ref = db.reference("/")

    def addDataToDB(self, jsonData):
        self.jsonData = jsonData
        id = str(uuid4())

        result = {id: self.jsonData}

        with open("data.json", 'r+') as file:
            data = json.load(file)
            data.update(result)
            file.seek(0)
            json.dump(data, file)

        f = open('data.json')
        jobsRef = self.ref.child('jobs')
        jobsRef.set(json.load(f))

    def getData(self):
        self.getRef = db.reference("jobs/")
        return self.getRef.get()
