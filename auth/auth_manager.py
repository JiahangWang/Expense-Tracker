import hashlib
import json
import os
import secrets

from core.user import User


class AuthManager:
    def __init__(self, users_file: str):
        self._users_file = users_file
        self._users: dict[str, dict] = {}
        self._load_users()

   
    def register(self, username: str, password: str) -> tuple[bool, str]:
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

    

    def _hash(self, password: str, salt: str) -> str:
        combined = (password + salt).encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    def _load_users(self) -> None:
        if not os.path.exists(self._users_file):
            self._users = {}
            return

        with open(self._users_file, "r") as f:
            self._users = json.load(f)

    def _save_users(self) -> None:
        os.makedirs(os.path.dirname(self._users_file), exist_ok=True)

        with open(self._users_file, "w") as f:
            json.dump(self._users, f, indent=4)

    def _ensure_user_data_dir(self, username: str) -> None:
        user_dir = os.path.join("data", username)
        os.makedirs(user_dir, exist_ok=True)
