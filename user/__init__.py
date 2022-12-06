class User:
    def __init__(self, username: str, email: str, password: str, salt: str) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt

    def to_json(self) -> dict[str, str]:
        return { "username": self.username, "email": self.email, "password": self.password, "salt": self.salt  }

    def __eq__(self, __o: object) -> bool:
        return (self.email == __o.email or self.username == __o.username)