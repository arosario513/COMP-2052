from flask_wtf import FlaskForm
from app.models import db
from app.models.user import User
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length


class Register(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=32)
        ],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ],
        render_kw={"placeholder": "Password"}
    )
    verify_password = PasswordField(
        "Verify Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ],
        render_kw={"placeholder": "Verify Password"}
    )
    submit = SubmitField("Create Account")

    def validate_username(self, username: StringField):
        if db.session.execute(
            db.select(User)
            .filter_by(username=username.data)
        ).first():
            raise ValidationError("User already exists")


class Login(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=32)
        ],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")
