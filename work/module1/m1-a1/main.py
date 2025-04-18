#!venv/bin/python

from flask import Flask, Response, jsonify, request
app: Flask = Flask(__name__)


@app.route("/info", methods=["GET"])
def info() -> Response:
    return jsonify(info="This is a basic API with only 2 paths: /info and /message")


@app.route("/message", methods=["POST"])
def message() -> Response:
    data = request.get_json()
    msg = data.get("input")
    return jsonify(input=msg)


if __name__ == "__main__":
    app.run(debug=True)
