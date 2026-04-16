# Description:
# This file stores shared configuration values for the Expense Tracker.
# It defines project paths, default login data, and fixed category/type options
# used throughout the application.

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
SAMPLE_DATA_FILE = DATA_DIR / "sample_data.csv"
DEFAULT_USERNAME = "Bob"
DEFAULT_PASSWORD = "123"

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
