# Description:
# This file provides analytics helpers for the Expense Tracker using pandas.
# It supports filtered summaries and yearly/monthly cashflow calculations.

import pandas as pd


def load_data(file_path):
    """
    Load one transaction CSV file into a DataFrame.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame()


def filter_data(file_path, transaction_type=None, year=None, month=None, day=None):
    """
    Load transaction data and apply optional type/date filters.
    """
    df = load_data(file_path)
    if df.empty:
        return df

    if transaction_type:
        df = df[df["type"] == transaction_type]

    if any(value and str(value) != "All" for value in (year, month, day)):
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

    if year and str(year) != "All":
        df = df[df["date"].dt.year == int(year)]
    if month and str(month) != "All":
        df = df[df["date"].dt.month == int(month)]
    if day and str(day) != "All":
        df = df[df["date"].dt.day == int(day)]

    return df


def category_summary(file_path, transaction_type=None, year=None, month=None, day=None):
    """
    Return grouped category totals for the current filter selection.
    """
    df = filter_data(file_path, transaction_type, year, month, day)
    if df.empty:
        return None
    return df.groupby("category")["amount"].sum()


def monthly_cashflow_summary(transactions, year):
    """
    Calculate monthly income, expense, and net values for one year.
    """
    monthly_income = [0.0] * 12
    monthly_expense = [0.0] * 12

    for transaction in transactions:
        try:
            date = pd.to_datetime(transaction.date, format="%Y-%m-%d", errors="raise")
        except ValueError:
            continue

        if date.year != year:
            continue

        month_index = date.month - 1
        if transaction.get_type() == "Income":
            monthly_income[month_index] += transaction.amount
        elif transaction.get_type() == "Expense":
            monthly_expense[month_index] += transaction.amount

    monthly_net = [income - expense for income, expense in zip(monthly_income, monthly_expense)]
    return monthly_income, monthly_expense, monthly_net


def yearly_cashflow_summary(transactions):
    """
    Calculate yearly income, expense, and net values across all years.
    """
    yearly_totals = {}

    for transaction in transactions:
        try:
            date = pd.to_datetime(transaction.date, format="%Y-%m-%d", errors="raise")
        except ValueError:
            continue

        year = int(date.year)
        yearly_totals.setdefault(year, {"income": 0.0, "expense": 0.0})

        if transaction.get_type() == "Income":
            yearly_totals[year]["income"] += transaction.amount
        elif transaction.get_type() == "Expense":
            yearly_totals[year]["expense"] += transaction.amount

    years = sorted(yearly_totals.keys())
    income_values = [yearly_totals[year]["income"] for year in years]
    expense_values = [yearly_totals[year]["expense"] for year in years]
    net_values = [income - expense for income, expense in zip(income_values, expense_values)]
    return years, income_values, expense_values, net_values
