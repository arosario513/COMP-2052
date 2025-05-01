#!venv/bin/python

from models.user import User
from models import db
from flask import Blueprint, request, url_for, redirect, render_template
from flask_login import login_user, logout_user, login_required
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

auth_blueprint = Blueprint("auth", __name__)
ph = PasswordHasher()

DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$cn6382O+GKdFP5HGFUqwCA$MazNjdUS2EOk96rL1tHseuf+GGS6mwOclCWozUgi3Aw"


@auth_blueprint.route("/register", methods=["GET", "POST"])
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


@auth_blueprint.route("/login", methods=["GET", "POST"])
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


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
