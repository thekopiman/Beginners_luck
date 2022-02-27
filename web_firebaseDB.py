from asyncio.windows_events import NULL
import firebase_admin
import os
from firebase_admin import db


from uuid import uuid4


class WebFireBaseDB():
    def __init__(self) -> None:
        '''
        Take note that for this class, u need to initialize it before you can use it
        as __init__ need to run. @classmethod will not be present for all the methods

        eg.
        hello = firebaseDB.FireBaseDB(update, context)
        hello.update_education(update, context)
        firebase_admin.delete_app(firebase_admin.get_app())

        '''
        self.cred_obj = firebase_admin.credentials.Certificate(
            rf'{os.path.dirname(os.path.realpath(__file__))}\<INSERT CERTIFICATE HERE>')
        self.default_app = firebase_admin.initialize_app(self.cred_obj, {
            'databaseURL': '<INSERT DATABASE URL HERE>'
        })

        self.ref = db.reference('/')

    def check_exisiting_user(self, username) -> bool:
        '''
        Check for duplicated usernames in the database
        '''

        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()

        all_user = []

        try:
            for key in list(users_ref_getdata.keys()):
                try:
                    all_user.append(users_ref_getdata[key]['username'])
                except KeyError:
                    continue
        except AttributeError:
            pass

        if str(username) in all_user:
            return True
        else:
            return False

    def register_account(self, username, password, full_name, education_cert, telegram_username=None, ):
        new_id = str(uuid4())

        users_ref = self.ref.child('users')

        users_ref.child(new_id).set({
            'web_id': str(new_id),
            'cert': str(education_cert),
            'full_name': str(full_name),
            'telegram_username': str(telegram_username),
            'username': str(username),
            'password': str(password),  # Hash it in the future
        })

    def register_job(self, company, description, jobSector, jobType, pay, qualification):
        new_id = str(uuid4())

        users_ref = self.ref.child('users')

        users_ref.child(new_id).set({
            'company': str(company),
            'description': str(description),
            'jobSector': str(jobSector),
            'jobType': str(jobType),
            'pay': str(pay),
            'qualification': str(qualification),

            # Hash it in the future
        })

    def get_login_details(self) -> dict:
        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()

        return_dict = {}
        for complex_id in users_ref_getdata:
            try:
                return_dict[users_ref_getdata[complex_id]['username']
                            ] = users_ref_getdata[complex_id]['password']

            except KeyError:
                continue

        return return_dict
