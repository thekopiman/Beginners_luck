# Import database module.
from asyncio.windows_events import NULL
import firebase_admin
import os
from firebase_admin import db
from telegram import Update
from telegram.ext import CallbackContext


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

        self.cred_obj = firebase_admin.credentials.Certificate(
            rf'{os.path.dirname(os.path.realpath(__file__))}\inteetsgintern-firebase-adminsdk-bh9du-ebdd137c22.json')
        self.default_app = firebase_admin.initialize_app(self.cred_obj, {
            'databaseURL': 'https://inteetsgintern-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })

        self.ref = db.reference('/')

    def updateuser(self, update: Update, context: CallbackContext) -> None:
        users_ref = self.ref.child('users')

        try:
            user_info = update.message.from_user
        except AttributeError:
            # print(update.callback_query.from_user)
            user_info = update.callback_query.from_user

        try:
            all_id = list(users_ref.get().keys())
        except AttributeError:
            all_id = []

        if str(user_info['id']) in all_id:
            pass  # Edit this ltr if there are missing data in the DB
        else:
            users_ref.child(str(user_info['id'])).set({
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

        if not str(user_id) in list(users_ref_getdata.keys()) and not str(user_id) in [users_ref_getdata[key]['telegram_id'] for key in list(users_ref_getdata.keys())]:
            self.updateuser(update, context)

        # users_ref.child(str(user_id)).update({'cert': update.message.text})
        users_ref.update({f'{str(user_id)}/cert': update.message.text})

    def update_full_name(self, update: Update, context: CallbackContext):
        users_ref = self.ref.child('users')
        users_ref_getdata = users_ref.get()

        if update.message.text == None:
            raise UnboundLocalError

        print("Yeetus", update.message.text)

        user_id = update.message.from_user.id

        if not str(user_id) in list(users_ref_getdata.keys()) and not str(user_id) in [users_ref_getdata[key]['telegram_id'] for key in list(users_ref_getdata.keys())]:
            self.updateuser(update, context)

        users_ref.update({f'{str(user_id)}/full_name': update.message.text})

        # users_ref.child(str(user_id)).update(
        #     {'full_name': update.message.text})
