#!venv/bin/python

from os import getenv
from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from models import db
from models.user import User

load_dotenv()

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

lm: LoginManager = LoginManager()
ph: PasswordHasher = PasswordHasher()

db.init_app(app)
lm.init_app(app)


@lm.user_loader
def load_user(uid: int):
    return User.query.get(uid)


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/register", methods=["GET", "POST"])
def register():
    error: str | None = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        verify_password = request.form.get("verify_password")
        if username and password:
            if User.query.filter_by(username=username).first():
                error = "User already exists"
            elif password != verify_password:
                error = "Passwords must match"
            else:
                hash = ph.hash(password)
                user = User(username=username, password=hash)

                db.session.add(user)
                db.session.commit()

                login_user(user)
                return redirect(url_for("dashboard"))
    return render_template("register.html", title="Register", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error: str | None = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            if username and password:
                user = User.query.filter_by(username=username).first()
                if user and ph.verify(user.password, password):
                    login_user(user)
                    return redirect(url_for("dashboard"))
                else:
                    error = "Invalid Login"
        except VerifyMismatchError:
            error = "Wrong Password"
    return render_template("login.html", title="Login", error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
