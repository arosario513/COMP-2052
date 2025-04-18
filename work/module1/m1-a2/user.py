class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "email": self.email}
