"""
Author: Perfect
Date: 2026-04-18
Description: Unit tests for analytics helpers and cashflow summary calculations.
"""

import pandas as pd

from core.analytics import (
    category_summary,
    filter_data,
    load_data,
    monthly_cashflow_summary,
    yearly_cashflow_summary,
)


class TestLoadAndFilterData:
    def test_load_data_builds_dataframe_from_transactions(self, monkeypatch, sample_transactions):
        monkeypatch.setattr("core.analytics.load_transactions", lambda user_ref: sample_transactions)

        df = load_data("bob")

        assert list(df.columns) == ["id", "amount", "date", "category", "type"]
        assert len(df) == 5
        assert df.iloc[0]["category"] == "salary"

    def test_filter_data_applies_type_and_date_filters(self, monkeypatch, sample_transactions):
        monkeypatch.setattr("core.analytics.load_transactions", lambda user_ref: sample_transactions)

        df = filter_data("bob", transaction_type="Expense", year="2026", month="04", day="02")

        assert len(df) == 2
        assert set(df["category"]) == {"food", "transport"}
        assert pd.api.types.is_datetime64_any_dtype(df["date"])

    def test_filter_data_returns_empty_dataframe_when_no_rows_match(self, monkeypatch, sample_transactions):
        monkeypatch.setattr("core.analytics.load_transactions", lambda user_ref: sample_transactions)

        df = filter_data("bob", transaction_type="Income", year="2024", month="01")

        assert df.empty


class TestCategorySummary:
    def test_category_summary_groups_amounts_by_category(self, monkeypatch, sample_transactions):
        monkeypatch.setattr("core.analytics.load_transactions", lambda user_ref: sample_transactions)

        summary = category_summary("bob", transaction_type="Expense", year="2026", month="04")

        assert summary is not None
        assert summary.to_dict() == {"food": 50.0, "transport": 25.0}

    def test_category_summary_returns_none_for_empty_result(self, monkeypatch):
        monkeypatch.setattr("core.analytics.load_transactions", lambda user_ref: [])

        assert category_summary("bob", transaction_type="Expense") is None


class TestCashflowSummaries:
    def test_monthly_cashflow_summary_aggregates_by_month(self, sample_transactions):
        income, expense, net = monthly_cashflow_summary(sample_transactions, 2026)

        assert income[3] == 3000.0
        assert expense[3] == 75.0
        assert net[3] == 2925.0
        assert income[4] == 200.0
        assert expense[4] == 0.0
        assert net[4] == 200.0

    def test_yearly_cashflow_summary_aggregates_across_years(self, sample_transactions):
        years, income, expense, net = yearly_cashflow_summary(sample_transactions)

        assert years == [2025, 2026]
        assert income == [0.0, 3200.0]
        assert expense == [100.0, 75.0]
        assert net == [-100.0, 3125.0]
