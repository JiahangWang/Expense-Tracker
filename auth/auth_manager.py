# Description:
# This file implements the authentication manager for the Expense Tracker.
# It supports registration, login, default-user setup, and account deletion
# while storing hashed passwords in a JSON file.

import hashlib
import json
import secrets
from pathlib import Path

from core.user import User


class AuthManager:
    def __init__(self, users_file: str):
        """
        Initialize the auth manager with a user storage file.
        """
        self._users_file = Path(users_file)
        self._users: dict[str, dict] = {}
        self._load_users()

    def register(self, username: str, password: str) -> tuple[bool, str]:
        """
        Register one new user account.
        """
        username = username.strip().lower()

        if not username or not password:
            return False, "Username and password cannot be empty."

        if username in self._users:
            return False, "Username already exists."

        salt = secrets.token_hex(16)
        password_hash = self._hash(password, salt)

        self._users[username] = {
            "password_hash": password_hash,
            "salt": salt,
        }
        self._save_users()
        self._ensure_user_data_dir(username)
        return True, "Registration successful."

    def login(self, username: str, password: str) -> tuple[bool, str, User | None]:
        """
        Validate credentials and return the matching user object.
        """
        username = username.strip().lower()

        if username not in self._users:
            return False, "Invalid username or password.", None

        stored = self._users[username]
        password_hash = self._hash(password, stored["salt"])

        if password_hash != stored["password_hash"]:
            return False, "Invalid username or password.", None

        user = User(
            username=username,
            password_hash=stored["password_hash"],
            salt=stored["salt"],
        )
        return True, "Login successful.", user

    def ensure_user(self, username: str, password: str) -> None:
        """
        Ensure one known user exists in storage.
        """
        username = username.strip().lower()
        if username in self._users:
            self._ensure_user_data_dir(username)
            return
        self.register(username, password)

    def delete_user(self, username: str) -> tuple[bool, str]:
        """
        Delete one user account and its personal data directory.
        """
        username = username.strip().lower()

        if username not in self._users:
            return False, "User not found."
        if len(self._users) <= 1:
            return False, "At least one user account must remain."

        del self._users[username]
        self._save_users()

        user_dir = self._user_dir(username)
        if user_dir.exists():
            for child in user_dir.iterdir():
                if child.is_file():
                    child.unlink()
            user_dir.rmdir()

        return True, "User deleted successfully."

    def list_usernames(self) -> list[str]:
        """
        Return all stored usernames.
        """
        return sorted(self._users.keys())

    def _hash(self, password: str, salt: str) -> str:
        """
        Hash one password using a salt.
        """
        combined = (password + salt).encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    def _load_users(self) -> None:
        """
        Load user data from the JSON storage file.
        """
        if not self._users_file.exists():
            self._users = {}
            return

        with open(self._users_file, "r", encoding="utf-8") as f:
            self._users = json.load(f)

    def _save_users(self) -> None:
        """
        Persist the in-memory user data to disk.
        """
        self._users_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self._users_file, "w", encoding="utf-8") as f:
            json.dump(self._users, f, indent=4)

    def _ensure_user_data_dir(self, username: str) -> None:
        """
        Ensure the personal data directory exists for one user.
        """
        self._user_dir(username).mkdir(parents=True, exist_ok=True)

    def _user_dir(self, username: str) -> Path:
        """
        Return the personal data directory for one user.
        """
        return self._users_file.parent / username
