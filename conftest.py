import os
import sys

import pytest

from core.transaction import Expense, Income


sys.path.insert(0, os.path.dirname(__file__))


@pytest.fixture
def valid_types():
    return ("Expense", "Income")


@pytest.fixture
def expense_categories():
    return ("food", "transport")


@pytest.fixture
def income_categories():
    return ("salary", "bonus")


@pytest.fixture
def sample_transactions():
    return [
        Income(1, 3000, "2026-04-01", "salary"),
        Expense(2, 50, "2026-04-02", "food"),
        Expense(3, 25, "2026-04-02", "transport"),
        Income(4, 200, "2026-05-01", "bonus"),
        Expense(5, 100, "2025-12-15", "food"),
    ]


@pytest.fixture
def april_expense_rows():
    return [
        {"id": 1, "date": "2026-04-18", "category": "transport", "amount": 20, "type": "Expense"},
        {"id": 3, "date": "2026-04-19", "category": "food", "amount": 50, "type": "Expense"},
    ]
