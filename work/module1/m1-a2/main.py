#!venv/bin/python

from flask import Flask, Response, jsonify, request
from user import User

app: Flask = Flask(__name__)

users: list[User] = [
    User("Alberto", "arosario@mail.com"),
    User("John", "jdoe@mail.com")
]


@app.route("/info", methods=["GET"])
def info() -> tuple[Response, int]:
    return jsonify(info="This API contains 3 paths", paths=["/adduser", "/info", "/users"]), 200


@app.route("/adduser", methods=["POST"])
def adduser() -> tuple[Response, int]:
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify(error="Incomplete data"), 400

    user: User = User(name, email)
    users.append(user)
    return jsonify(message=f"User '{user.name}' successfully added"), 200


@app.route("/users", methods=["GET"])
def get_users() -> tuple[Response, int]:
    return jsonify([i.to_dict() for i in users]), 200


if __name__ == "__main__":
    app.run(debug=True)
