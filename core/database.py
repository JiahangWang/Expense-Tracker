import csv
import json
import os
from contextlib import closing
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

from config.app_config import DATA_DIR, USERS_FILE
from core.transaction import Transaction

load_dotenv()

_INITIALIZED = False


def _server_config(include_database: bool) -> dict:
    config = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
    }
    if include_database:
        config["database"] = os.getenv("DB_NAME", "expense_tracker")
    return config


def _connect(include_database: bool = True):
    return mysql.connector.connect(**_server_config(include_database))


def ensure_database_ready() -> None:
    global _INITIALIZED
    if _INITIALIZED:
        return

    _create_database()
    _create_tables()
    _bootstrap_legacy_data()
    _INITIALIZED = True


def _create_database() -> None:
    database_name = os.getenv("DB_NAME", "expense_tracker")
    with closing(_connect(include_database=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        connection.commit()


def _create_tables() -> None:
    with closing(_connect()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    salt VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    record_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    transaction_id INT NOT NULL,
                    amount DECIMAL(12, 2) NOT NULL,
                    transaction_date DATE NOT NULL,
                    category VARCHAR(255) NOT NULL,
                    transaction_type ENUM('Expense', 'Income') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_user_transaction (user_id, transaction_id),
                    CONSTRAINT fk_transactions_user
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        ON DELETE CASCADE
                )
                """
            )
        connection.commit()


def _bootstrap_legacy_data() -> None:
    with closing(_connect()) as connection:
        with closing(connection.cursor(dictionary=True)) as cursor:
            cursor.execute("SELECT COUNT(*) AS user_count FROM users")
            row = cursor.fetchone()
            if row and row["user_count"] > 0:
                return

        legacy_users = _load_legacy_users()
        if not legacy_users:
            return

        with closing(connection.cursor()) as cursor:
            for username, credentials in legacy_users.items():
                cursor.execute(
                    """
                    INSERT INTO users (username, password_hash, salt)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        username,
                        credentials["password_hash"],
                        credentials["salt"],
                    ),
                )

            connection.commit()

        for username in legacy_users:
            legacy_csv = DATA_DIR / username / "data.csv"
            if legacy_csv.exists():
                user = _fetch_user_no_init(username)
                if user is not None:
                    _replace_transactions_for_user_id(
                        int(user["id"]),
                        _load_legacy_transactions(legacy_csv),
                    )


def _load_legacy_users() -> dict[str, dict]:
    if not USERS_FILE.exists():
        return {}

    with USERS_FILE.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    return {
        str(username).strip().lower(): {
            "password_hash": str(values["password_hash"]),
            "salt": str(values["salt"]),
        }
        for username, values in data.items()
    }


def _load_legacy_transactions(csv_path: Path) -> list[Transaction]:
    transactions = []
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        next_generated_id = 1

        for row in reader:
            transaction_id_raw = str(row.get("id", "")).strip()
            if transaction_id_raw:
                transaction_id = int(transaction_id_raw)
                next_generated_id = max(next_generated_id, transaction_id + 1)
            else:
                transaction_id = next_generated_id
                next_generated_id += 1

            transaction = Transaction.from_dict(
                {
                    "id": transaction_id,
                    "amount": row["amount"],
                    "date": row["date"],
                    "category": row["category"],
                    "type": row["type"],
                }
            )
            transactions.append(transaction)

    return transactions


def _normalize_username(user_ref) -> str:
    if hasattr(user_ref, "username"):
        return str(user_ref.username).strip().lower()

    user_text = str(user_ref).strip()
    if not user_text:
        raise ValueError("A username or user reference is required.")

    normalized = user_text.replace("\\", "/")
    if normalized.endswith("/data.csv"):
        return Path(normalized).parts[-2].strip().lower()

    return Path(normalized).name.strip().lower()


def fetch_user(username: str) -> dict | None:
    ensure_database_ready()
    return _fetch_user_no_init(username)


def _fetch_user_no_init(username: str) -> dict | None:
    with closing(_connect()) as connection:
        with closing(connection.cursor(dictionary=True)) as cursor:
            cursor.execute(
                """
                SELECT id, username, password_hash, salt
                FROM users
                WHERE username = %s
                """,
                (username.strip().lower(),),
            )
            return cursor.fetchone()


def create_user(username: str, password_hash: str, salt: str) -> int:
    ensure_database_ready()
    normalized_username = username.strip().lower()

    with closing(_connect()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, salt)
                VALUES (%s, %s, %s)
                """,
                (normalized_username, password_hash, salt),
            )
            connection.commit()
            return int(cursor.lastrowid)


def delete_user(username: str) -> bool:
    ensure_database_ready()
    with closing(_connect()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "DELETE FROM users WHERE username = %s",
                (username.strip().lower(),),
            )
            connection.commit()
            return cursor.rowcount > 0


def list_usernames() -> list[str]:
    ensure_database_ready()
    with closing(_connect()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT username FROM users ORDER BY username")
            return [row[0] for row in cursor.fetchall()]


def count_users() -> int:
    ensure_database_ready()
    with closing(_connect()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            row = cursor.fetchone()
            return int(row[0]) if row else 0


def fetch_transactions(user_ref) -> list[dict]:
    ensure_database_ready()
    username = _normalize_username(user_ref)

    with closing(_connect()) as connection:
        with closing(connection.cursor(dictionary=True)) as cursor:
            cursor.execute(
                """
                SELECT
                    t.transaction_id AS id,
                    CAST(t.amount AS DOUBLE) AS amount,
                    DATE_FORMAT(t.transaction_date, '%Y-%m-%d') AS date,
                    t.category AS category,
                    t.transaction_type AS type
                FROM transactions AS t
                INNER JOIN users AS u ON u.id = t.user_id
                WHERE u.username = %s
                ORDER BY t.transaction_date, t.transaction_id
                """,
                (username,),
            )
            return cursor.fetchall()


def replace_transactions(user_ref, transactions: list[Transaction]) -> None:
    ensure_database_ready()
    username = _normalize_username(user_ref)
    user = fetch_user(username)
    if user is None:
        raise ValueError(f"User '{username}' does not exist.")

    _replace_transactions_for_user_id(int(user["id"]), transactions)


def _replace_transactions_for_user_id(user_id: int, transactions: list[Transaction]) -> None:
    with closing(_connect()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("DELETE FROM transactions WHERE user_id = %s", (user_id,))

            if transactions:
                rows = [
                    (
                        user_id,
                        int(transaction.transaction_id),
                        float(transaction.amount),
                        transaction.date,
                        transaction.category,
                        transaction.get_type(),
                    )
                    for transaction in transactions
                ]
                cursor.executemany(
                    """
                    INSERT INTO transactions
                        (user_id, transaction_id, amount, transaction_date, category, transaction_type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    rows,
                )

        connection.commit()


def check_connection() -> tuple[bool, str]:
    try:
        ensure_database_ready()
    except Error as exc:
        return False, str(exc)
    return True, "MySQL connection successful."
