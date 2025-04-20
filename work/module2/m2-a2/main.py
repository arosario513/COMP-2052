#!venv/bin/python

from flask import Flask, render_template
from login import Login
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def index():
    return login()


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    return render_template("index.html", title="Form Validation", form=form)


if __name__ == "__main__":
    app.run(debug=True)
