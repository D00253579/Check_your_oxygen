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


class UserWarnings(db.Document):
    meta = {"collection": "userWarnings"}
    current_temperature = db.IntField()
    current_notification = db.StringField()
    current_action = db.StringField()
    sent_at = db.DateTimeField(default=datetime.datetime.now)


class Warnings(db.Document):
    meta = {"collection": "warnings"}
    temperature = db.IntField()
    message = db.StringField()
    action = db.StringField()


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


def add_User_Warning(current_temperature):
    if current_temperature is not False:
        current_notification = get_notification(current_temperature)
        current_action = get_action(current_notification)
        UserWarnings(
            current_temperature=current_temperature,
            current_notification=current_notification,
            current_action=current_action,
        ).save()
    else:
        print("Cannot add user warning")


def get_notification(current_temperature):
    if int(current_temperature) < 7:
        warning = Warnings.objects.get(
            message="EXTREME TEMPERATURE WARNING ABNORMAL COLD LEVELS"
        )
    elif int(current_temperature) > 35:
        warning = Warnings.objects.get(
            message="EXTREME TEMPERATURE WARNING ABNORMAL HEAT LEVELS"
        )
    elif int(current_temperature) <= 14 or int(current_temperature) >= 31:
        warning = Warnings.objects.get(message="WARNING! Air Quality Poor")
    elif int(current_temperature) >= 20 and int(current_temperature) <= 26:
        warning = Warnings.objects.get(message="Oxygen levels are normal")
    else:
        warning = Warnings.objects.get(message="Air quality depleting")

    if warning:
        return warning.message
    else:
        return "No notification present"


def get_action(current_notification):
    if current_notification == "EXTREME TEMPERATURE WARNING ABNORMAL COLD LEVELS":
        actionMessage = Warnings.objects.get(
            action="Keep doors open to stop the trapping of pollutants"
        )
    elif current_notification == "EXTREME TEMPERATURE WARNING ABNORMAL HEAT LEVELS":
        actionMessage = Warnings.objects.get(
            action="Keep windows closed and open doors"
        )
    elif current_notification == "WARNING! Air Quality Poor":
        actionMessage = Warnings.objects.get(action="Open a window")
    elif current_notification == "Oxygen levels are normal":
        actionMessage = Warnings.objects.get(action="Nothing to worry about :)")
    else:
        actionMessage = Warnings.objects.get(action="Keep an eye on levels")

    if actionMessage:
        return actionMessage.action
    else:
        return "No action present"


def get_current_user_warning():
    current_user_warning = UserWarnings.objects.order_by("-sent_at").first()

    return {
        "current_warning": [
            {
                "current_temperature": current_user_warning.current_temperature,
                "current_notification": current_user_warning.current_notification,
                "current_action": current_user_warning.current_action,
            }
        ]
    }
