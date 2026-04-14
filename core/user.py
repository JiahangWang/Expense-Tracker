import os


class User:
    def __init__(self, username: str, password_hash: str, salt: str):
        self._username = username
        self._password_hash = password_hash
        self._salt = salt

    @property
    def username(self) -> str:
        return self._username

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def salt(self) -> str:
        return self._salt

    @property
    def data_path(self) -> str:
        return os.path.join("data", self._username, "data.csv")

    def to_dict(self) -> dict:
        return {
            "username": self._username,
            "password_hash": self._password_hash,
            "salt": self._salt,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            username=str(data["username"]),
            password_hash=str(data["password_hash"]),
            salt=str(data["salt"]),
        )

    def __repr__(self) -> str:
        return f"User(username={self._username})"
