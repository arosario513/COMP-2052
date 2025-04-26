#!venv/bin/python

from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from os import getenv
from dotenv import load_dotenv
from user import User


load_dotenv()

# Don't ever do this in production!
users = {
    "admin": "$argon2id$v=19$m=65536,t=3,p=4$ODQvwLeEfBZ5lqLyIdTd/g$22JgukFXYbvp07bI51oqs7D9mo5He9MGtW/a8LTB9WI",
}

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

lm: LoginManager = LoginManager()
lm.init_app(app)

ph: PasswordHasher = PasswordHasher()


@lm.user_loader
def load_user(uid):
    if uid in users:
        return User(uid)
    return "User not found"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Home"), 200


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            if username in users and ph.verify(users[username], password):
                user: User = User(username)
                login_user(user)
                print("[+] Valid")
                return redirect(url_for("dashboard"))
        except VerifyMismatchError:
            print("[!] Not Valid")
    return render_template("login.html", title="Login"), 200


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard"), 200


if __name__ == "__main__":
    app.run(debug=True)
