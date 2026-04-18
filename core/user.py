# Description:
# This file defines the User model used by the authentication layer.
# It stores hashed credential data and exposes the user's personal data path.

import os
from pathlib import Path


class User:
    def __init__(self, username: str, password_hash: str, salt: str, user_id: int | None = None):
        """
        Initialize one user object.
        """
        self._user_id = user_id
        self._username = username
        self._password_hash = password_hash
        self._salt = salt

    @property
    def user_id(self) -> int | None:
        """
        Return the database user ID when available.
        """
        return self._user_id

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
        Return one legacy-compatible identifier for the user's transactions.
        """
        return os.path.join("data", self._username, "data.csv")

    @property
    def data_file(self) -> Path:
        """
        Return one legacy-compatible transaction identifier as a Path object.
        """
        return Path(self.data_path)

    def to_dict(self) -> dict:
        """
        Convert the user object to a serializable dictionary.
        """
        return {
            "user_id": self._user_id,
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
            user_id=int(data["user_id"]) if data.get("user_id") is not None else None,
            username=str(data["username"]),
            password_hash=str(data["password_hash"]),
            salt=str(data["salt"]),
        )

    def __repr__(self) -> str:
        return f"User(user_id={self._user_id}, username={self._username})"
