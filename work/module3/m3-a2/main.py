from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from os import getenv
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_principal import (
    AnonymousIdentity, Identity,
    Permission, PermissionDenied,
    Principal, RoleNeed,
    UserNeed, identity_changed,
    identity_loaded
)

from user import User

load_dotenv()

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

lm: LoginManager = LoginManager()
lm.init_app(app)
pr: Principal = Principal(app)

ph: PasswordHasher = PasswordHasher()

admin_access = Permission(RoleNeed("Admin"))
mod_access = Permission(RoleNeed("Moderator"))

# Don't do this in production!
users = {
    "admin": {
        "hash": "$argon2id$v=19$m=65536,t=3,p=4$ODQvwLeEfBZ5lqLyIdTd/g$22JgukFXYbvp07bI51oqs7D9mo5He9MGtW/a8LTB9WI",
        "roles": ["Admin", "Moderator"]
    },
    "user": {
        "hash": "$argon2id$v=19$m=65536,t=3,p=4$81qySwL8yqQniC4u9JM+VQ$47kgEZPkM3EOeamtRTYOnN5zyvsL/PoSVgNvWAhZaGk",
        "roles": []
    },
    "mod": {
        "hash": "$argon2id$v=19$m=65536,t=3,p=4$a6irYXNegd66nO7CUg2V8A$cs0Mn8zB5b/6qF2d5kn2IbSRJZQLChzs6pBivtQ7IXs",
        "roles": ["Moderator"]
    }
}


@lm.user_loader
def load_user(uid):
    user = users.get(uid)
    if user:
        return User(uid, user["roles"])
    return None


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity: Identity):
    user = load_user(identity.id)
    if user is not None:
        identity.provides.add(UserNeed(user.id))
        for role in user.roles:
            identity.provides.add(RoleNeed(role))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Home"), 200


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            if username in users and ph.verify(users[username]["hash"], password):
                user = User(username, roles=users[username]["roles"])
                login_user(user)
                identity_changed.send(app, identity=Identity(user.id))
                print("[+] Valid")
                return redirect(url_for("dashboard"))
        except VerifyMismatchError:
            print("[!] Not valid")
    return render_template("login.html", title="Login"), 200


@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard"), 200


@app.route("/admin")
@admin_access.require()
def admin():
    return render_template("admin.html", title="Admin Actions"), 200


@app.route("/moderation")
@mod_access.require()
def moderation():
    return render_template("mod.html", title="Moderator Settings"), 200


@app.errorhandler(PermissionDenied)
def permission_denied(e):
    return render_template("error.html", title="Error 403", error="Permission Denied"), 403


@app.errorhandler(404)
def error404(e):
    return render_template("error.html", title="Error 404", error="Page not Found"), 404


if __name__ == "__main__":
    app.run(debug=True)
