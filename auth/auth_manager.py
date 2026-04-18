"""
Author: Jiahang
Date: 2026-04-12
Description: Authentication manager for registration, login, and user-account operations.
"""

import hashlib
import secrets

from core.database import count_users, create_user, delete_user, fetch_user, list_usernames
from core.user import User


class AuthManager:
    def __init__(self, users_file: str | None = None):
        """
        Initialize the auth manager.

        The users_file argument is kept for backward compatibility, but
        credential storage now lives in MySQL.
        """
        self._users_file = users_file

    def register(self, username: str, password: str) -> tuple[bool, str]:
        """
        Register one new user account.
        """
        username = username.strip().lower()

        if not username or not password:
            return False, "Username and password cannot be empty."

        if fetch_user(username) is not None:
            return False, "Username already exists."

        salt = secrets.token_hex(16)
        password_hash = self._hash(password, salt)
        create_user(username, password_hash, salt)
        return True, "Registration successful."

    def login(self, username: str, password: str) -> tuple[bool, str, User | None]:
        """
        Validate credentials and return the matching user object.
        """
        username = username.strip().lower()
        stored = fetch_user(username)

        if stored is None:
            return False, "Invalid username or password.", None

        password_hash = self._hash(password, stored["salt"])
        if password_hash != stored["password_hash"]:
            return False, "Invalid username or password.", None

        user = User(
            user_id=int(stored["id"]),
            username=stored["username"],
            password_hash=stored["password_hash"],
            salt=stored["salt"],
        )
        return True, "Login successful.", user

    def ensure_user(self, username: str, password: str) -> None:
        """
        Ensure one known user exists in storage.
        """
        username = username.strip().lower()
        if fetch_user(username) is None:
            self.register(username, password)

    def delete_user(self, username: str) -> tuple[bool, str]:
        """
        Delete one user account and its transactions.
        """
        username = username.strip().lower()

        if fetch_user(username) is None:
            return False, "User not found."
        if count_users() <= 1:
            return False, "At least one user account must remain."

        delete_user(username)
        return True, "User deleted successfully."

    def list_usernames(self) -> list[str]:
        """
        Return all stored usernames.
        """
        return list_usernames()

    def _hash(self, password: str, salt: str) -> str:
        """
        Hash one password using a salt.
        """
        combined = (password + salt).encode("utf-8")
        return hashlib.sha256(combined).hexdigest()
