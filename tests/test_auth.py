import os
import pytest
from auth.auth_manager import AuthManager


USERS_FILE = "data/test_users.json"


@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists(USERS_FILE):
        os.remove(USERS_FILE)


@pytest.fixture
def auth():
    return AuthManager(USERS_FILE)




class TestRegister:
    def test_register_success(self, auth):
        ok, msg = auth.register("alice", "pass123")
        assert ok
        assert msg == "Registration successful."

    def test_register_duplicate_username(self, auth):
        auth.register("alice", "pass123")
        ok, msg = auth.register("alice", "newpass")
        assert not ok
        assert "already exists" in msg

    def test_register_empty_username(self, auth):
        ok, msg = auth.register("", "pass123")
        assert not ok

    def test_register_empty_password(self, auth):
        ok, msg = auth.register("alice", "")
        assert not ok

    def test_register_empty_both(self, auth):
        ok, msg = auth.register("", "")
        assert not ok

    def test_register_creates_user_data_dir(self, auth):
        auth.register("alice", "pass123")
        assert os.path.isdir(os.path.join("data", "alice"))

    def test_register_username_is_case_insensitive(self, auth):
        auth.register("Alice", "pass123")
        ok, msg = auth.register("alice", "pass123")
        assert not ok




class TestLogin:
    def test_login_success(self, auth):
        auth.register("alice", "pass123")
        ok, msg, user = auth.login("alice", "pass123")
        assert ok
        assert user is not None
        assert user.username == "alice"

    def test_login_wrong_password(self, auth):
        auth.register("alice", "pass123")
        ok, msg, user = auth.login("alice", "wrongpass")
        assert not ok
        assert user is None

    def test_login_nonexistent_user(self, auth):
        ok, msg, user = auth.login("ghost", "pass123")
        assert not ok
        assert user is None

    def test_login_case_insensitive_username(self, auth):
        auth.register("alice", "pass123")
        ok, msg, user = auth.login("ALICE", "pass123")
        assert ok
        assert user.username == "alice"

    def test_login_returns_correct_user_object(self, auth):
        auth.register("alice", "pass123")
        _, _, user = auth.login("alice", "pass123")
        assert user.username == "alice"
        assert user.password_hash != "pass123"
        assert user.data_path == os.path.join("data", "alice", "data.csv")



class TestSecurity:
    def test_passwords_are_not_stored_in_plaintext(self, auth):
        import json
        auth.register("alice", "pass123")
        with open(USERS_FILE) as f:
            data = json.load(f)
        assert data["alice"]["password_hash"] != "pass123"

    def test_different_users_same_password_have_different_hashes(self, auth):
        import json
        auth.register("alice", "samepass")
        auth.register("bob", "samepass")
        with open(USERS_FILE) as f:
            data = json.load(f)
        assert data["alice"]["password_hash"] != data["bob"]["password_hash"]
