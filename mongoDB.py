from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, IntField
import base64
import datetime
import bcrypt

# from .__init__ import db
from __init__ import db


class Users(db.Document):
    meta = {"collection": "users"}
    first_name = db.StringField()
    last_name = db.StringField()
    user_email = db.EmailField()
    user_password = db.StringField()


def hashPassword(password):
    hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashedPassword.decode()


def add_user(firstName, lastName, email, password):
    if firstName and lastName and email and password is not False:
        hashedPassword = hashPassword(password)
        Users(
            first_name=firstName,
            last_name=lastName,
            user_email=email,
            user_password=hashedPassword,
        ).save()


def check_users(email, password):
    doesUserExist = False
    for user in Users.objects:
        if user.user_email.lower() == email.lower():
            if bcrypt.checkpw(password.encode(), user.user_password.encode()):
                doesUserExist = True
                break

    return doesUserExist
