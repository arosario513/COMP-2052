#!venv/bin/python

from os import getenv
from flask import Flask, render_template
from flask_login import (
    LoginManager,
    login_required,
)
from dotenv import load_dotenv
from auth import auth_blueprint
from models import db
from models.user import User
from werkzeug.exceptions import HTTPException

load_dotenv()

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.register_blueprint(auth_blueprint)

lm: LoginManager = LoginManager()


db.init_app(app)
lm.init_app(app)


@lm.user_loader
def load_user(uid: int):
    return db.session.get(User, uid)


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@app.errorhandler(HTTPException)
def unauthorized(e):
    return render_template(
        "error.html",
        title=f"Error {e.code}",
        err_msg=e.description
    ), e.code


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
