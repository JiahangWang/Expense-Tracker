"""
Author: Jiahang
Date: 2026-04-11
Description: Shared configuration values for project paths and transaction category options.
"""

from pathlib import Path


# Resolve project-level paths once so every module can import the same locations.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
DATA_BACKUP_DIR = BASE_DIR / "data_backup"
BACKUP_USERS_FILE = DATA_BACKUP_DIR / "users.json"

INCOME_CATEGORIES = (
    "salary",
    "freelance",
    "bonus",
    "interest",
)

EXPENSE_CATEGORIES = (
    "food",
    "transport",
    "shopping",
    "utilities",
    "health",
    "entertainment",
    "rent",
    "insurance",
)

TRANSACTION_TYPES = ("Expense", "Income")
