# Description:
# This file defines the User model used by the authentication layer.
# It stores hashed credential data and exposes the user's personal data path.

import os
from pathlib import Path


class User:
    def __init__(self, username: str, password_hash: str, salt: str):
        """
        Initialize one user object.
        """
        self._username = username
        self._password_hash = password_hash
        self._salt = salt

    @property
    def username(self) -> str:
        """
        Return the username.
        """
        return self._username

    @property
    def password_hash(self) -> str:
        """
        Return the stored password hash.
        """
        return self._password_hash

    @property
    def salt(self) -> str:
        """
        Return the password salt.
        """
        return self._salt

    @property
    def data_path(self) -> str:
        """
        Return the user's transaction CSV path as a string.
        """
        return os.path.join("data", self._username, "data.csv")

    @property
    def data_file(self) -> Path:
        """
        Return the user's transaction CSV path as a Path object.
        """
        return Path(self.data_path)

    def to_dict(self) -> dict:
        """
        Convert the user object to a serializable dictionary.
        """
        return {
            "username": self._username,
            "password_hash": self._password_hash,
            "salt": self._salt,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """
        Build a user object from a dictionary.
        """
        return cls(
            username=str(data["username"]),
            password_hash=str(data["password_hash"]),
            salt=str(data["salt"]),
        )

    def __repr__(self) -> str:
        return f"User(username={self._username})"
