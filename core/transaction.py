"""
Author: Jiahang
Date: 2026-04-11
Description: Transaction model classes for shared, income, and expense-specific behavior.
"""

class Transaction:
    def __init__(self, transaction_id: int, amount: float, date: str, category: str):
        """
        Initialize a transaction object.
        """
        self._transaction_id = transaction_id
        self._amount = amount
        self._date = date
        self._category = category

    @property
    def transaction_id(self) -> int:
        """
        Return the transaction ID.
        """
        return self._transaction_id

    @property
    def amount(self) -> float:
        """
        Return the transaction amount.
        """
        return self._amount

    @property
    def date(self) -> str:
        """
        Return the transaction date.
        """
        return self._date

    @property
    def category(self) -> str:
        """
        Return the transaction category.
        """
        return self._category

    def get_type(self) -> str:
        """
        Return the transaction type label.
        """
        return "Transaction"

    def get_signed_amount(self) -> float:
        """
        Return the signed amount used for balance calculations.
        """
        return self._amount

    def to_dict(self) -> dict:
        """
        Convert the transaction object to a dictionary.
        """
        return {
            "id": self._transaction_id,
            "amount": self._amount,
            "date": self._date,
            "category": self._category,
            "type": self.get_type(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """
        Build the correct transaction object from serialized data.
        """
        transaction_type = str(data["type"])
        transaction_id = int(data["id"])
        amount = float(data["amount"])
        date = str(data["date"])
        category = str(data["category"])

        if transaction_type == "Expense":
            return Expense(transaction_id, amount, date, category)
        if transaction_type == "Income":
            return Income(transaction_id, amount, date, category)
        return cls(transaction_id, amount, date, category)

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self._transaction_id}, amount={self._amount}, "
            f"date={self._date}, category={self._category}, type={self.get_type()})"
        )


class Expense(Transaction):
    def get_type(self) -> str:
        """
        Return the transaction type for expenses.
        """
        return "Expense"

    def get_signed_amount(self) -> float:
        """
        Return the signed amount for an expense.
        """
        return -self.amount


class Income(Transaction):
    def get_type(self) -> str:
        """
        Return the transaction type for income.
        """
        return "Income"
