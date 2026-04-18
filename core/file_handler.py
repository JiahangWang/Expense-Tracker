"""
Author: Jiahang
Date: 2026-04-13
Description: Compatibility wrapper that keeps transaction load/save calls stable over MySQL storage.
"""

from core.database import fetch_transactions, replace_transactions
from core.transaction import Transaction


def save_transactions(user_ref, transactions):
    """
    Save one user's transactions to MySQL.
    """
    replace_transactions(user_ref, transactions)


def load_transactions(user_ref):
    """
    Load one user's transactions from MySQL and recreate transaction objects.
    """
    return [Transaction.from_dict(row) for row in fetch_transactions(user_ref)]
