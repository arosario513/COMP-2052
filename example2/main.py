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

DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$cn6382O+GKdFP5HGFUqwCA$MazNjdUS2EOk96rL1tHseuf+GGS6mwOclCWozUgi3Aw"

db.init_app(app)
lm.init_app(app)


@lm.user_loader
def load_user(uid: int):
    return db.session.get(User, uid)


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

        if not username or not password or not verify_password:
            error = "Fill out all fields"

        if db.session.execute(
            db.select(User)
            .filter_by(username=username)
        ).first():
            error = "User already exists"

        elif password != verify_password:
            assert password is not None
            error = "Passwords must match"

        else:
            assert password is not None
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

        if not username or not password:
            error = "Fill out all fields"

        else:
            user = User.query.filter_by(username=username).first()

            assert password is not None

            # This is to avoid timing attacks. I know, it's overkill.
            user_hash = user.password if user else DUMMY_HASH

            try:
                is_valid_password = ph.verify(user_hash, password)
            except VerifyMismatchError:
                is_valid_password = False

            if is_valid_password and user:
                login_user(user)
                return redirect(url_for("dashboard"))

            elif user:
                error = "Wrong Password"

            else:
                error = "Invalid Login"

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
