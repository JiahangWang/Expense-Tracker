"""
Author: Jiahang
Date: 2026-04-18
Description: Shared pytest configuration and reusable fixtures for the test suite.
"""

import os
import sys

import pytest

from core.transaction import Expense, Income


# Make the repository root importable when pytest discovers tests from the project root.
sys.path.insert(0, os.path.dirname(__file__))


@pytest.fixture
def valid_types():
    """Return supported transaction types used by validation-oriented tests."""
    return ("Expense", "Income")


@pytest.fixture
def expense_categories():
    """Return a compact set of expense categories for reusable form tests."""
    return ("food", "transport")


@pytest.fixture
def income_categories():
    """Return a compact set of income categories for reusable form tests."""
    return ("salary", "bonus")


@pytest.fixture
def sample_transactions():
    """Return a reusable transaction list shared by analytics-focused tests."""
    return [
        Income(1, 3000, "2026-04-01", "salary"),
        Expense(2, 50, "2026-04-02", "food"),
        Expense(3, 25, "2026-04-02", "transport"),
        Income(4, 200, "2026-05-01", "bonus"),
        Expense(5, 100, "2025-12-15", "food"),
    ]


@pytest.fixture
def april_expense_rows():
    """Return the expected filtered rows for one sample April expense view."""
    return [
        {"id": 1, "date": "2026-04-18", "category": "transport", "amount": 20, "type": "Expense"},
        {"id": 3, "date": "2026-04-19", "category": "food", "amount": 50, "type": "Expense"},
    ]
