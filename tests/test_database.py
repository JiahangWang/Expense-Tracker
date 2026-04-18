"""
Author: Jiahang
Date: 2026-04-18
Description: Unit tests for backup-user loading helpers used during seed setup.
"""

from core.database import _load_backup_users


def test_load_backup_users_reads_all_valid_users(monkeypatch, tmp_path):
    backup_users = tmp_path / "users.json"
    backup_users.write_text(
        (
            "{"
            '"bob": {"password_hash": "hash123", "salt": "salt123"},'
            '"naku": {"password_hash": "hash456", "salt": "salt456"},'
            '"perfect": {"password_hash": "hash789", "salt": "salt789"}'
            "}"
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("core.database.BACKUP_USERS_FILE", backup_users)

    assert _load_backup_users() == {
        "bob": {"password_hash": "hash123", "salt": "salt123"},
        "naku": {"password_hash": "hash456", "salt": "salt456"},
        "perfect": {"password_hash": "hash789", "salt": "salt789"},
    }


def test_load_backup_users_returns_empty_dict_when_file_missing(monkeypatch, tmp_path):
    monkeypatch.setattr("core.database.BACKUP_USERS_FILE", tmp_path / "missing.json")

    assert _load_backup_users() == {}


def test_load_backup_users_skips_invalid_entries(monkeypatch, tmp_path):
    backup_users = tmp_path / "users.json"
    backup_users.write_text(
        (
            "{"
            '"bob": {"password_hash": "hash123", "salt": "salt123"},'
            '"broken": {"password_hash": "hash456"},'
            '"oops": "not-an-object"'
            "}"
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("core.database.BACKUP_USERS_FILE", backup_users)

    assert _load_backup_users() == {
        "bob": {"password_hash": "hash123", "salt": "salt123"},
    }
