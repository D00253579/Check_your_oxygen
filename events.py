from extensions import socketio

import mongoDB


@socketio.on("connect")
def handle_connect():
    print("Socket connected!")


@socketio.on("updateTemp")
def update_temperature(newTemp):
    print("NEW TEMPERATURE: ", newTemp)
    mongoDB.add_User_Warning(newTemp)
