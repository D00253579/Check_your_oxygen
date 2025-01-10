import os
import pathlib
import requests
from flask import Flask, render_template, session, abort, redirect, request
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

# from . import mongoDB
# from . import mongoDB
import mongoDB
import pb

# from .config import config
from config import config

load_dotenv()
app = Flask(__name__)
app.secret_key = config.get("APP_SECRET_KEY")
database_URI = os.getenv("DATABASE_URI")
app.config["MONGODB_SETTINGS"] = {"host": database_URI}

db = MongoEngine()
db.init_app(app)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = config.get("GOOGLE_CLIENT_ID")
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, ".client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="http://127.0.0.1:5000/callback",
    # redirect_uri="https://checkyouroxygen.online/callback",
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorisation required error
        else:
            return function()

    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def add_user():
    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    email = request.form.get("email")
    password = request.form.get("password")
    if first_name and last_name and email and password:
        mongoDB.add_user(first_name, last_name, email, password)
        return redirect("/main_page")
    else:
        return "Not all fields were filled!!"


@app.route("/login")
def googleLogin():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/normal_login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    check_user = mongoDB.check_users(email, password)
    print(check_user)
    if check_user is True:
        return redirect("/main_page")
    else:
        return redirect("/")


@app.route("/main_page")
def main_Page():
    return render_template("mainPage.html")


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # States don't match

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    print(session["google_id"])
    print(session["name"])
    return redirect("/main_page")


if __name__ == "__main__":
    app.run(debug=True)
