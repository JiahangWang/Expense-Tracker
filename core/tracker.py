# Description:
# This file defines the ExpenseTracker class, which manages a collection of
# transactions and provides balance, lookup, and delete operations.

class ExpenseTracker:
    def __init__(self):
        """
        Initialize the tracker with an empty transaction list.
        """
        self.transactions = []

    def add_transaction(self, transaction):
        """
        Add one transaction to the tracker.
        """
        self.transactions.append(transaction)

    def get_next_transaction_id(self):
        """
        Return the next available transaction ID.
        """
        if not self.transactions:
            return 1
        return max(transaction.transaction_id for transaction in self.transactions) + 1

    def get_balance(self):
        """
        Calculate the current balance using all tracked transactions.
        """
        total_balance = 0.0
        for transaction in self.transactions:
            total_balance += transaction.get_signed_amount()
        return total_balance

    def get_all_transactions(self):
        """
        Return all tracked transactions.
        """
        return self.transactions

    def get_transaction_by_id(self, transaction_id):
        """
        Find one transaction by its ID.
        """
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction
        return None

    def delete_transaction_by_id(self, transaction_id):
        """
        Delete one transaction by its ID.
        """
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction is None:
            return False
        self.transactions.remove(transaction)
        return True
