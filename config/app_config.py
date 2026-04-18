# Description:
# This file stores shared configuration values for the Expense Tracker.
# It defines project paths and fixed category/type options
# used throughout the application.

from pathlib import Path


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
