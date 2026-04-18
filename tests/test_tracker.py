from core.tracker import ExpenseTracker
from core.transaction import Expense, Income


class TestExpenseTracker:
    def test_get_next_transaction_id_is_one_when_empty(self):
        tracker = ExpenseTracker()

        assert tracker.get_next_transaction_id() == 1

    def test_get_next_transaction_id_tracks_highest_existing_id(self):
        tracker = ExpenseTracker()
        tracker.add_transaction(Income(3, 1000, "2026-04-01", "salary"))
        tracker.add_transaction(Expense(8, 50, "2026-04-02", "food"))

        assert tracker.get_next_transaction_id() == 9

    def test_get_balance_combines_income_and_expense_signed_amounts(self):
        tracker = ExpenseTracker()
        tracker.add_transaction(Income(1, 1000, "2026-04-01", "salary"))
        tracker.add_transaction(Expense(2, 125.5, "2026-04-02", "food"))
        tracker.add_transaction(Expense(3, 74.5, "2026-04-03", "transport"))

        assert tracker.get_balance() == 800.0

    def test_get_transaction_by_id_returns_matching_transaction(self):
        tracker = ExpenseTracker()
        transaction = Income(7, 300, "2026-04-01", "bonus")
        tracker.add_transaction(transaction)

        assert tracker.get_transaction_by_id(7) is transaction
        assert tracker.get_transaction_by_id(99) is None

    def test_delete_transaction_by_id_removes_existing_transaction(self):
        tracker = ExpenseTracker()
        transaction = Expense(5, 40, "2026-04-01", "food")
        tracker.add_transaction(transaction)

        assert tracker.delete_transaction_by_id(5) is True
        assert tracker.get_all_transactions() == []

    def test_delete_transaction_by_id_returns_false_for_missing_transaction(self):
        tracker = ExpenseTracker()

        assert tracker.delete_transaction_by_id(123) is False

