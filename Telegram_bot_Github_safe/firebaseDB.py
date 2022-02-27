# Import database module.
from asyncio.windows_events import NULL
import firebase_admin
import os
from firebase_admin import db
from numpy import append
from telegram import Update
from telegram.ext import CallbackContext
from uuid import uuid4


class FireBaseDB():
    def __init__(self, update: Update, context: CallbackContext) -> None:
        '''
        Take note that for this class, u need to initialize it before you can use it
        as __init__ need to run. @classmethod will not be present for all the methods

        eg.
        hello = firebaseDB.FireBaseDB(update, context)
        hello.update_education(update, context)
        firebase_admin.delete_app(firebase_admin.get_app())

        '''
        print('hello')
        self.update = update
        self.context = context
        self.new_id = str(uuid4())

        self.cred_obj = firebase_admin.credentials.Certificate(
            rf'{os.path.dirname(os.path.realpath(__file__))}<INSERT CERTIFICATE HERE>')  # You may put it in the same folder as this firebaseDB.py file, just add the certificate name here eg. hello.json
        self.default_app = firebase_admin.initialize_app(self.cred_obj, {
            'databaseURL': '<INSERT DATABASE URL HERE>'
        })

        self.ref = db.reference('/')

    def obtain_main_id(self, user_data, telegram_id) -> str:
        telegram_id = str(telegram_id)
        try:
            for complex_id in dict(user_data):
                if user_data[complex_id]['telegram_id'] == telegram_id:
                    return complex_id

            return str(uuid4())
        except (TypeError, KeyError):
            return str(uuid4())

    def obtain_main_id_web(self, user_data, telegram_id) -> str:
        telegram_id = str(telegram_id)
        try:
            for complex_id in dict(user_data):
                if user_data[complex_id]['web_id'] == telegram_id:
                    return complex_id

            return str(uuid4())
        except (TypeError, KeyError):
            return str(uuid4())

    def check_unique_identifier(self, update: Update, context: CallbackContext):
        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()
        user_identifier = update.message.text

        try:
            user_info = update.message.from_user
        except AttributeError:
            # print(update.callback_query.from_user)
            user_info = update.callback_query.from_user

        try:
            user_info['username']
        except KeyError:
            user_info['username'] = None

        all_id = []
        try:
            for key in list(users_ref_getdata.keys()):
                try:
                    all_id.append(users_ref_getdata[key]['web_id'])
                except KeyError:
                    continue
        except AttributeError:
            pass

        if str(user_identifier) in all_id:
            true_id = self.obtain_main_id_web(
                users_ref_getdata, str(user_identifier))
            print("user_identifier", user_identifier)
            users_ref.child(str(true_id)).update({
                'telegram_id': user_info['id'],
                'telegram_name': {
                    'first_name': user_info['first_name'],
                    'last_name': user_info['last_name']
                },
                'telegram_username': user_info['username']
            })

            return users_ref_getdata[true_id]['full_name']
        else:
            return False

    def check_existing_user(self, update: Update, context: CallbackContext) -> bool:
        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()

        try:
            user_info = update.message.from_user

        except AttributeError:
            # print(update.callback_query.from_user)
            user_info = update.callback_query.from_user

        all_id = []
        try:
            for key in list(users_ref_getdata.keys()):
                try:
                    all_id.append(users_ref_getdata[key]['telegram_id'])
                except KeyError:
                    continue
        except AttributeError:
            pass

        if str(user_info['id']) in all_id:
            self.new_id = self.obtain_main_id(
                users_ref_getdata, user_info['id'])
            users_ref.update(
                {f'{str(self.new_id)}/telegram_name/': update.message.text})

            return users_ref_getdata[self.new_id]['full_name']
        else:
            return False

    def updateuser(self, update: Update, context: CallbackContext) -> None:
        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()

        try:
            user_info = update.message.from_user
        except AttributeError:
            # print(update.callback_query.from_user)
            user_info = update.callback_query.from_user

        all_id = []
        try:
            for key in list(users_ref_getdata.keys()):
                try:
                    all_id.append(users_ref_getdata[key]['telegram_id'])
                except KeyError:
                    continue
        except AttributeError:
            pass

        self.new_id = self.obtain_main_id(users_ref_getdata, user_info['id'])

        if str(user_info['id']) in all_id:
            pass  # Edit this ltr if there are missing data in the DB
        else:
            users_ref.child(self.new_id).set({
                'telegram_username': user_info['username'],
                'telegram_id': str(user_info['id']),
                'password': None,
                'full_name': None,
                'cert': None,
                'telegram_name': {
                    'first_name': user_info['first_name'],
                    'last_name': user_info['last_name']
                }
            })

    def update_education(self, update: Update, context: CallbackContext):
        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()

        if update.message.text == None:
            raise UnboundLocalError

        user_id = update.message.from_user.id
        self.new_id = self.obtain_main_id(users_ref_getdata, user_id)

        all_id = []
        try:
            for key in list(users_ref_getdata.keys()):
                try:
                    all_id.append(users_ref_getdata[key]['telegram_id'])
                except KeyError:
                    continue
        except AttributeError:
            pass

        if not str(user_id) in list(users_ref_getdata.keys()) and not str(user_id) in all_id:
            self.updateuser(update, context)

        # users_ref.child(str(user_id)).update({'cert': update.message.text})
        users_ref.update({f'{str(self.new_id)}/cert': update.message.text})

    def update_full_name(self, update: Update, context: CallbackContext):
        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()

        if update.message.text == None:
            raise UnboundLocalError

        print("Yeetus", update.message.text)

        user_id = update.message.from_user.id
        self.new_id = self.obtain_main_id(users_ref_getdata, user_id)

        all_id = []
        try:
            for key in list(users_ref_getdata.keys()):
                try:
                    all_id.append(users_ref_getdata[key]['telegram_id'])
                except KeyError:
                    continue
        except AttributeError:
            pass

        if not str(user_id) in list(users_ref_getdata.keys()) and not str(user_id) in all_id:
            self.updateuser(update, context)

        users_ref.update(
            {f'{str(self.new_id)}/full_name': update.message.text})
        print(users_ref_getdata)

        # users_ref.child(str(user_id)).update(
        #     {'full_name': update.message.text})

    def getjobs(self, update: Update, context: CallbackContext) -> list:
        jobs_ref = self.ref.child('jobs')
        jobs_ref_getdata = jobs_ref.get()
        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()

        try:
            user_info = update.message.from_user
            self.new_id = self.obtain_main_id(
                users_ref_getdata, user_info['id'])
        except AttributeError:
            # print(update.callback_query.from_user)
            user_info = update.callback_query.from_user
            self.new_id = self.obtain_main_id(
                users_ref_getdata, user_info['id'])

        print('user_info', user_info)
        complex_id = self.obtain_main_id(users_ref_getdata, user_info['id'])
        user_education = users_ref_getdata[complex_id]['cert']

        lst_of_jobs = []

        cert_level = ['Degree', 'Diploma', 'A levels', 'O/N levels']

        for jobs_id in jobs_ref_getdata:
            if cert_level.index(user_education) <= cert_level.index(jobs_ref_getdata[jobs_id]['qualification']):
                lst_of_jobs.append(jobs_ref_getdata[jobs_id])

        return lst_of_jobs
