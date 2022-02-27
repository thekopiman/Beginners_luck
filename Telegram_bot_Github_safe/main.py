from cgitb import text
import logging
from matplotlib.font_manager import list_fonts
from telegram import CallbackQuery, User, parsemode
from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ForceReply
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
import random
import os
import sqlite3
import firebaseDB
import firebase_admin


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class main():
    def __init__(self, token) -> None:
        # # Create the Updater and pass it your bot's token.
        self.EXPECT_NAME, self.EXPECT_BUTTON_CLICK, self.EXPECT_EDUCATION, self.EXPECT_EDUCATION_BUTTON = range(
            4)

        self.EXPECT_IDENTIFIER = 4

        updater = Updater(token)
        # # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start))

        existing_login_handler = ConversationHandler(
            entry_points=[CommandHandler('weblogin', self.weblogin)],
            states={
                self.EXPECT_IDENTIFIER: [MessageHandler(Filters.text, self.unique_identifier_by_user)],

            },
            fallbacks=[CommandHandler('cancel', self.cancel)]

        )
        new_login_handler = ConversationHandler(
            entry_points=[CommandHandler('createuser', self.createuser)],
            states={
                self.EXPECT_NAME: [MessageHandler(Filters.text, self.name_input_by_user)],
                self.EXPECT_EDUCATION: [MessageHandler(
                    Filters.regex('^(Degree|Diploma|A levels|O/N levels)$'), self.education_level)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]

        )

        dispatcher.add_handler(new_login_handler)
        dispatcher.add_handler(existing_login_handler)
        dispatcher.add_handler(CommandHandler("getjobs", self.getjobs))
        updater.start_polling()

        updater.idle()

    def start(self, update: Update, context: CallbackContext) -> None:
        '''Start messages'''

        hello = firebaseDB.FireBaseDB(update, context)

        false_or_fullname = hello.check_existing_user(update, context)

        if (false_or_fullname != False):
            update.message.reply_text(
                f'''
                Welcome back {false_or_fullname}, I hope that you are looking for a new job/internship. Click /getjobs now!
                '''
            )
        else:
            update.message.reply_text(
                'Hi! Welcome to Inteet SG Intern Telegram Bot!')
            update.message.reply_text(
                '''
                If you have not created a profile in the website, you may create a basic profile here now by clicking /createuser
                ''')
            update.message.reply_text(
                '''
                However, if you have created an account via the website, please key in the unique identifier found on the website after clicking /weblogin
                ''')

        firebase_admin.delete_app(firebase_admin.get_app())

        DBUpdateLocal.updateuser(update, context)

    def weblogin(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Please key in the unique indentifier found on the website'
            'Send /cancel to stop this conversation.\n\n'
        )
        update.message.reply_text(

            text='Unique identifier?',
            reply_markup=ForceReply(),
        )

        return self.EXPECT_IDENTIFIER

    def unique_identifier_by_user(self, update: Update, context: CallbackContext):
        ''' The user's reply to the name prompt comes here  '''
        self.identifier = update.message.text
        logger.info("Your identifier is %s", self.identifier)
        update.message.reply_text(
            'Checking Database...'
        )
        hello = firebaseDB.FireBaseDB(update, context)
        false_or_fullname = hello.check_unique_identifier(update, context)

        if (false_or_fullname != False):
            update.message.reply_text(
                f'''
                Welcome back {false_or_fullname}, I hope that you are looking for a new job/internship.
                '''
            )
        else:
            update.message.reply_text(
                'Sorry... we are unable to find your profile. The unique identifier is case and space sensitive, you may try against by clicking /weblogin')
            update.message.reply_text(
                '''
                However, you your data still cannot be found, please create a new account by clicking /createuser
                ''')

        firebase_admin.delete_app(firebase_admin.get_app())

        DBUpdateLocal.update_full_name(update, context)

        return ConversationHandler.END

    def createuser(self, update: Update, context: CallbackContext):
        hello = firebaseDB.FireBaseDB(update, context)
        hello.updateuser(update, context)
        firebase_admin.delete_app(firebase_admin.get_app())

        DBUpdateLocal.updateuser(update, context)
        update.message.reply_text(
            'Please answer several basic questions about yourself!'
            'Send /cancel to stop this conversation.\n\n'
        )
        update.message.reply_text(

            text='What is your full name?',
            reply_markup=ForceReply(),
        )

        return self.EXPECT_NAME

    def name_input_by_user(self, update: Update, context: CallbackContext):
        ''' The user's reply to the name prompt comes here  '''
        self.name = update.message.text
        logger.info("Wow, your name is %s", self.name)

        hello = firebaseDB.FireBaseDB(update, context)
        hello.update_full_name(update, context)
        firebase_admin.delete_app(firebase_admin.get_app())

        DBUpdateLocal.update_full_name(update, context)

        # saves the name
        context.user_data['name'] = self.name
        update.message.reply_text(f'Your name is saved as {self.name[:100]}')

        # ends this particular conversation flow
        education_level = [['Degree', 'Diploma', 'A levels', 'O/N levels']]

        # n_cols = 1 is for single column and mutliple rows
        update.message.reply_text(
            text='Highest Qualification', reply_markup=ReplyKeyboardMarkup(
                education_level, one_time_keyboard=True, input_field_placeholder='Your highest qualification?'
            ))
        return self.EXPECT_EDUCATION

    def education_level(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        # print(user)
        logger.info("Certificate of %s: %s", self.name, update.message.text)
        if update.message.text in ['Degree', 'Diploma', 'A levels', 'O/N levels']:
            hello = firebaseDB.FireBaseDB(update, context)
            hello.update_education(update, context)
            firebase_admin.delete_app(firebase_admin.get_app())

            DBUpdateLocal.update_education(update, context)
        update.message.reply_text(
            'I see! Remember to check for new jobs with /getjobs',
        )
        return ConversationHandler.END

    def getjobs(self, update: Update, context: CallbackContext):
        hello = firebaseDB.FireBaseDB(update, context)
        jobs_available = hello.getjobs(update, context)
        firebase_admin.delete_app(firebase_admin.get_app())

        if jobs_available == []:
            update.message.reply_text(
                'There are no jobs available for you')
        else:
            for jobs_dict in jobs_available:
                company = jobs_dict['company']
                description = jobs_dict['description']
                jobSector = jobs_dict['jobSector']
                pay = jobs_dict['pay']
                qualification = jobs_dict['qualification']
                update.message.reply_text(
                    f'''
                company = {company} \n
                description = {description} \n
                jobSector = {jobSector} \n
                pay = {pay} \n
                qualification = {qualification} \n
                ''')

    def cancel(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Name Conversation cancelled by user. Bye. Send /createuser to start again')
        return ConversationHandler.END


class DBUpdateLocal():
    def __init__(self, update: Update, context: CallbackContext):
        self.directory = r"C: \Users\User\Desktop\Coding\Projects\NTU IEEE Hackathon\Telegram_bot\DataBase\\"
        self.update = update
        self.context = context
        self.content = context.args

    @classmethod
    def updateuser(self, update: Update, context: CallbackContext) -> None:
        directory = os.path.dirname(os.path.realpath(__file__)) + "\DataBase\\"

        try:
            user_info = update.message.from_user
        except AttributeError:
            # print(update.callback_query.from_user)
            user_info = update.callback_query.from_user

        # print(directory)
        if os.path.isfile(f'{directory}Users.sqlite'):
            conn = sqlite3.connect(f'{directory}Users.sqlite')
            cur = conn.cursor()
        else:
            conn = sqlite3.connect(f'{directory}Users.sqlite')
            cur = conn.cursor()
            cur.execute(
                'CREATE TABLE "Users" ("id"	INTEGER,"first_name" TEXT, "last_name" TEXT, "username" TEXT, "realname" Text, "education" Text, "password" Text);')

        cur.execute('SELECT id from Users')
        all_id = [x[0] for x in cur.fetchall()]
        if user_info['id'] in all_id:
            pass
        else:
            cur.execute('INSERT INTO Users (id,first_name,last_name,username) VALUES (?,?,?,?);', (
                user_info['id'], user_info['first_name'], user_info['last_name'], user_info['username']))

        conn.commit()

    @classmethod
    def update_education(self, update: Update, context: CallbackContext):
        directory = os.path.dirname(os.path.realpath(__file__)) + "\DataBase\\"

        # print(query.data)

        if update.message.text == None:
            raise UnboundLocalError

        user_id = update.message.from_user.id
        # print(f'{self.directory}{str(user_id)}.sqlite')
        if os.path.isfile(f'{directory}Users.sqlite'):
            conn = sqlite3.connect(f'{directory}Users.sqlite')
            cur = conn.cursor()
        else:
            self.updateuser(update, context)  # Create a new user here!
            conn = sqlite3.connect(f'{directory}Users.sqlite')
            cur = conn.cursor()

        # cur.execute('SELECT Users from Users')
        # print(cur.fetchall())
        print(update.message.text,  user_id)
        cur.execute("UPDATE Users SET education = ? WHERE id = ?;",
                    (update.message.text, user_id))

        cur.execute('SELECT * from Users')

        conn.commit()
        # update.message.reply_text("The timing has been updated!")

    @classmethod
    def update_full_name(self, update: Update, context: CallbackContext):
        directory = os.path.dirname(os.path.realpath(__file__)) + "\DataBase\\"

        # print(query.data)

        if update.message.text == None:
            raise UnboundLocalError

        user_id = update.message.from_user.id
        # print(f'{self.directory}{str(user_id)}.sqlite')
        if os.path.isfile(f'{directory}Users.sqlite'):
            conn = sqlite3.connect(f'{directory}Users.sqlite')
            cur = conn.cursor()
        else:
            self.updateuser(update, context)  # Create a new user here!
            conn = sqlite3.connect(f'{directory}Users.sqlite')
            cur = conn.cursor()

        # cur.execute('SELECT Users from Users')
        # print(cur.fetchall())
        print(update.message.text,  user_id)
        cur.execute("UPDATE Users SET realname = ? WHERE id = ?;",
                    (update.message.text, user_id))

        cur.execute('SELECT * from Users')

        conn.commit()


if __name__ == '__main__':
    token = "<INSERT TELEGRAM TOKEN HERE>"

    start1 = main(token=token)
