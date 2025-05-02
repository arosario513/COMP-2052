#!venv/bin/python

from app.auth.forms import Register, Login
from app.models.user import User
from app.models import db
from flask import url_for, redirect, render_template, flash
from flask_login import login_user, logout_user, login_required
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from . import auth_blueprint

ph = PasswordHasher()

DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$cn6382O+GKdFP5HGFUqwCA$MazNjdUS2EOk96rL1tHseuf+GGS6mwOclCWozUgi3Aw"


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        assert password is not None
        hash = ph.hash(password)
        user = User(username=username, password=hash)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect(url_for("main.dashboard"))
    return render_template("register.html", title="Register", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
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
            flash("Logged in", "success")
            return redirect(url_for("main.dashboard"))

        elif user:
            flash("Wrong password", "danger")
        else:
            flash("Invalid login", "danger")

    return render_template("login.html", title="Login", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "warning")
    return redirect(url_for("auth.login"))
