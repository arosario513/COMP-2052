from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, roles=None):
        self.id = id
        self.roles = roles or []

    def __repr__(self) -> str:
        return f"<User {self.id} {self.roles}>"

    def has_role(self, role: str) -> bool:
        return role in self.roles
