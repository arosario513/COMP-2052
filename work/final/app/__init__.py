from app.admin.routes import admin_blueprint
from app.appointments.routes import appointment_blueprint
from app.auth.routes import auth_blueprint
from app.models import db
from app.models.user import User
from app.routes import main as main_blueprint
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_principal import Principal
from os import getenv
from werkzeug.exceptions import HTTPException


load_dotenv()

lm: LoginManager = LoginManager()
pr: Principal = Principal()


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)
    lm.init_app(app)
    pr.init_app(app)

    with app.app_context():
        db.create_all()
        db.add_roles(["Admin", "Patient", "Doctor"])
        db.add_admin()

    @lm.user_loader
    def load_user(uid: int):
        return db.session.get(User, uid)

    @app.errorhandler(HTTPException)
    def unauthorized(e):
        return render_template(
            "error.html",
            title=f"Error {e.code}",
            err_msg=e.description
        ), e.code

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(appointment_blueprint)
    from app import security
    return app
