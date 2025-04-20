from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class Login(FlaskForm):
    user = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(
                min=3
            )
        ],
        render_kw={
            "class": "form-control mb-2",
            "placeholder": "Username"
        }
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired()
        ],
        render_kw={
            "class": "form-control mb-2",
            "placeholder": "Email"
        }
    )

    passwd = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)],
        render_kw={
            "class": "form-control mb-2",
            "placeholder": "Password"
        }
    )

    submit = SubmitField(
        "Login",
        render_kw={
            "class": "btn btn-primary w-100"
        }
    )
