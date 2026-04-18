"""
Author: Jiahang
Date: 2026-04-18
Description: Unit tests for transaction serialization and subtype behavior.
"""

from core.transaction import Expense, Income, Transaction


class TestTransaction:
    def test_to_dict_returns_expected_shape(self):
        transaction = Transaction(1, 12.5, "2026-04-18", "misc")

        assert transaction.to_dict() == {
            "id": 1,
            "amount": 12.5,
            "date": "2026-04-18",
            "category": "misc",
            "type": "Transaction",
        }

    def test_from_dict_builds_income(self):
        transaction = Transaction.from_dict(
            {"id": 2, "amount": 1500, "date": "2026-04-01", "category": "salary", "type": "Income"}
        )

        assert isinstance(transaction, Income)
        assert transaction.transaction_id == 2
        assert transaction.amount == 1500.0
        assert transaction.get_signed_amount() == 1500.0

    def test_from_dict_builds_expense(self):
        transaction = Transaction.from_dict(
            {"id": 3, "amount": 88, "date": "2026-04-02", "category": "food", "type": "Expense"}
        )

        assert isinstance(transaction, Expense)
        assert transaction.transaction_id == 3
        assert transaction.amount == 88.0
        assert transaction.get_signed_amount() == -88.0

    def test_from_dict_falls_back_to_base_transaction_for_unknown_type(self):
        transaction = Transaction.from_dict(
            {"id": 4, "amount": 20, "date": "2026-04-03", "category": "other", "type": "Other"}
        )

        assert type(transaction) is Transaction
        assert transaction.get_type() == "Transaction"
