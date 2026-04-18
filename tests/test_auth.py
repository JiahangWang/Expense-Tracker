from auth.auth_manager import AuthManager


class FakeDatabase:
    def __init__(self):
        self.users = {}
        self.next_user_id = 1

    def fetch_user(self, username):
        return self.users.get(username.strip().lower())

    def create_user(self, username, password_hash, salt):
        normalized = username.strip().lower()
        user_id = self.next_user_id
        self.next_user_id += 1
        self.users[normalized] = {
            "id": user_id,
            "username": normalized,
            "password_hash": password_hash,
            "salt": salt,
        }
        return user_id

    def delete_user(self, username):
        normalized = username.strip().lower()
        return self.users.pop(normalized, None) is not None

    def list_usernames(self):
        return sorted(self.users.keys())

    def count_users(self):
        return len(self.users)


def build_auth(monkeypatch):
    fake_db = FakeDatabase()
    monkeypatch.setattr("auth.auth_manager.fetch_user", fake_db.fetch_user)
    monkeypatch.setattr("auth.auth_manager.create_user", fake_db.create_user)
    monkeypatch.setattr("auth.auth_manager.delete_user", fake_db.delete_user)
    monkeypatch.setattr("auth.auth_manager.list_usernames", fake_db.list_usernames)
    monkeypatch.setattr("auth.auth_manager.count_users", fake_db.count_users)
    return AuthManager(), fake_db


class TestRegister:
    def test_register_success(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        ok, msg = auth.register("alice", "pass123")
        assert ok
        assert msg == "Registration successful."

    def test_register_duplicate_username(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        auth.register("alice", "pass123")
        ok, msg = auth.register("alice", "newpass")
        assert not ok
        assert "already exists" in msg

    def test_register_empty_username(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        ok, msg = auth.register("", "pass123")
        assert not ok
        assert "cannot be empty" in msg

    def test_register_empty_password(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        ok, msg = auth.register("alice", "")
        assert not ok
        assert "cannot be empty" in msg

    def test_register_empty_both(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        ok, msg = auth.register("", "")
        assert not ok
        assert "cannot be empty" in msg

    def test_register_username_is_case_insensitive(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        auth.register("Alice", "pass123")
        ok, msg = auth.register("alice", "pass123")
        assert not ok
        assert "already exists" in msg


class TestLogin:
    def test_login_success(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        auth.register("alice", "pass123")
        ok, msg, user = auth.login("alice", "pass123")
        assert ok
        assert msg == "Login successful."
        assert user is not None
        assert user.username == "alice"

    def test_login_wrong_password(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        auth.register("alice", "pass123")
        ok, msg, user = auth.login("alice", "wrongpass")
        assert not ok
        assert msg == "Invalid username or password."
        assert user is None

    def test_login_nonexistent_user(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        ok, msg, user = auth.login("ghost", "pass123")
        assert not ok
        assert msg == "Invalid username or password."
        assert user is None

    def test_login_case_insensitive_username(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        auth.register("alice", "pass123")
        ok, msg, user = auth.login("ALICE", "pass123")
        assert ok
        assert msg == "Login successful."
        assert user is not None
        assert user.username == "alice"

    def test_login_returns_correct_user_object(self, monkeypatch):
        auth, _ = build_auth(monkeypatch)
        auth.register("alice", "pass123")
        _, _, user = auth.login("alice", "pass123")
        assert user is not None
        assert user.username == "alice"
        assert user.password_hash != "pass123"
        assert user.user_id == 1


class TestSecurity:
    def test_passwords_are_not_stored_in_plaintext(self, monkeypatch):
        auth, fake_db = build_auth(monkeypatch)
        auth.register("alice", "pass123")
        assert fake_db.users["alice"]["password_hash"] != "pass123"

    def test_different_users_same_password_have_different_hashes(self, monkeypatch):
        auth, fake_db = build_auth(monkeypatch)
        auth.register("alice", "samepass")
        auth.register("bob", "samepass")
        assert fake_db.users["alice"]["password_hash"] != fake_db.users["bob"]["password_hash"]
