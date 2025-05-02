from flask import Blueprint, render_template
from flask_login import (
    login_required,
)
from werkzeug.exceptions import HTTPException

main: Blueprint = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html", title="Home")


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@main.errorhandler(HTTPException)
def unauthorized(e):
    return render_template(
        "error.html",
        title=f"Error {e.code}",
        err_msg=e.description
    ), e.code
