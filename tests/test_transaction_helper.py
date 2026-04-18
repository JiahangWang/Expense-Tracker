import pytest

from core.transaction import Expense, Income
from core.transaction_helper import (
    build_transaction_rows,
    format_transaction_lines,
    matches_period,
    validate_transaction_input,
)


VALID_TYPES = ("Expense", "Income")
EXPENSE_CATEGORIES = ("food", "transport")
INCOME_CATEGORIES = ("salary", "bonus")


class TestValidateTransactionInput:
    def test_returns_normalized_values_for_valid_input(self):
        result = validate_transaction_input(
            "12.50",
            "2026-04-18",
            "food",
            "Expense",
            VALID_TYPES,
            EXPENSE_CATEGORIES,
        )

        assert result == (12.5, "2026-04-18", "food", "Expense")

    @pytest.mark.parametrize(
        ("amount_raw", "date_text", "category", "transaction_type", "message"),
        [
            ("", "2026-04-18", "food", "Expense", "required"),
            ("12", "2026-04-18", "food", "Other", "valid transaction type"),
            ("12", "2026-04-18", "rent", "Expense", "dropdown"),
            ("abc", "2026-04-18", "food", "Expense", "number"),
            ("0", "2026-04-18", "food", "Expense", "greater than 0"),
            ("12", "04/18/2026", "food", "Expense", "YYYY-MM-DD"),
        ],
    )
    def test_rejects_invalid_input(self, amount_raw, date_text, category, transaction_type, message):
        with pytest.raises(ValueError, match=message):
            validate_transaction_input(
                amount_raw,
                date_text,
                category,
                transaction_type,
                VALID_TYPES,
                EXPENSE_CATEGORIES,
            )


class TestPeriodHelpers:
    def test_matches_period_supports_all_wildcards(self):
        assert matches_period("2026-04-18", "All", "All", "All") is True

    def test_matches_period_filters_by_year_month_and_day(self):
        assert matches_period("2026-04-18", "2026", "04", "18") is True
        assert matches_period("2026-04-18", "2025", "04", "18") is False
        assert matches_period("2026-04-18", "2026", "03", "18") is False
        assert matches_period("2026-04-18", "2026", "04", "17") is False

    def test_matches_period_returns_false_for_invalid_date(self):
        assert matches_period("bad-date", "2026", "04", "18") is False


class TestBuildAndFormatRows:
    def test_build_transaction_rows_filters_and_sorts_rows(self):
        transactions = [
            Expense(3, 50, "2026-04-19", "food"),
            Expense(1, 20, "2026-04-18", "transport"),
            Income(2, 1000, "2026-04-18", "salary"),
            Expense(4, 80, "2026-03-18", "food"),
        ]

        rows = build_transaction_rows(transactions, "Expense", "2026", "04", "All")

        assert rows == [
            {"id": 1, "date": "2026-04-18", "category": "transport", "amount": 20, "type": "Expense"},
            {"id": 3, "date": "2026-04-19", "category": "food", "amount": 50, "type": "Expense"},
        ]

    def test_format_transaction_lines_builds_fixed_width_output(self):
        output = format_transaction_lines(
            [{"id": 1, "date": "2026-04-18", "category": "food", "amount": 12.5, "type": "Expense"}]
        )

        assert "ID" in output
        assert "2026-04-18" in output
        assert "food" in output
        assert "12.50" in output
        assert "Expense" in output

