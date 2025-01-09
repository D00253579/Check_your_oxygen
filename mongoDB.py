from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, IntField
import base64
import datetime

# from .__init__ import db
from __init__ import db


class Users(db.Document):
    meta = {"collection": "users"}
    first_name = db.StringField()
    last_name = db.StringField()
    user_email = db.EmailField()
    user_password = db.StringField()


def add_user(firstName, lastName, email, password):
    if firstName and lastName and email and password is not False:
        Users(
            first_name=firstName,
            last_name=lastName,
            user_email=email,
            user_password=password,
        ).save()
