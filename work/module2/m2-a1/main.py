#!venv/bin/activate

from flask import Flask, render_template

app: Flask = Flask(__name__)

names = {
    "First Name": ["Alberto", "John"],
    "Last Name": ["Rosario", "Doe"]
}


@app.route("/", methods=["GET"])
def index():
    return render_template("./index.html", title="Home", data=names)


if __name__ == "__main__":
    app.run(debug=True)
