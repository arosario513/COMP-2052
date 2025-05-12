from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from dotenv import load_dotenv
from os import getenv

load_dotenv()

ph: PasswordHasher = PasswordHasher()


class Database(SQLAlchemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_roles(self, roles: list[str]):
        from app.models.role import Role
        for i in roles:
            if not self.session.execute(
                    self.select(Role).filter_by(name=i)
            ).first():
                self.session.add(Role(name=i))
        self.session.commit()

    def add_admin(self):
        from app.models.user import User
        first_name: str | None = getenv("ADMIN_FIRSTNAME")
        last_name: str | None = getenv("ADMIN_LASTNAME")
        email: str | None = getenv("ADMIN_EMAIL")
        password: str | None = getenv("ADMIN_PASSWORD")
        if not first_name:
            raise ValueError(
                "ADMIN_FIRSTNAME must be set in the environment."
            )
        if not last_name:
            raise ValueError(
                "ADMIN_LASTNAME must be set in the environment."
            )
        if not email:
            raise ValueError(
                "ADMIN_EMAIL must be set in the environment."
            )
        if not password:
            raise ValueError(
                "ADMIN_PASSWORD must be set in the environment."
            )
        admin = User.query.filter_by(email=email).first()

        if not admin:
            hash = ph.hash(password)
            admin = User(first_name, last_name, email, hash)

            self.session.add(admin)
            self.session.commit()

            admin.add_role("Admin")
            self.session.commit()


db: Database = Database()
