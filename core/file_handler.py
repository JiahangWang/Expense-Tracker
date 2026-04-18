# Description:
# This file provides functions to save and load transaction data using MySQL.
# The function names are kept stable so the UI layer can keep calling them.

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
