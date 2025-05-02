from app.auth.routes import auth_blueprint
from app.models import db
from app.models.user import User
from app.routes import main as main_blueprint
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from os import getenv

load_dotenv()

lm: LoginManager = LoginManager()


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)
    lm.init_app(app)

    @lm.user_loader
    def load_user(uid: int):
        return db.session.get(User, uid)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    return app
