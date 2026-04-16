class ExpenseTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_next_transaction_id(self):
        if not self.transactions:
            return 1
        return max(transaction.transaction_id for transaction in self.transactions) + 1

    def get_balance(self):
        total_balance = 0.0
        for transaction in self.transactions:
            total_balance += transaction.get_signed_amount()
        return total_balance

    def get_all_transactions(self):
        return self.transactions

    def get_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction
        return None

    def delete_transaction_by_id(self, transaction_id):
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction is None:
            return False
        self.transactions.remove(transaction)
        return True
