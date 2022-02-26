
# Import database module.
import firebase_admin
import os
from firebase_admin import db
from datetime import datetime


cred_obj = firebase_admin.credentials.Certificate(
    rf'{os.path.dirname(os.path.realpath(__file__))}\inteetsgintern-firebase-adminsdk-bh9du-ebdd137c22.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://inteetsgintern-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a database reference to our posts
ref = db.reference('/')

users_ref = ref.child('users')
users_ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})

# print(users_ref.get().keys())
