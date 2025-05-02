#!venv/bin/python
from app import create_app
from app.models import db
from flask import Flask

app: Flask = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
