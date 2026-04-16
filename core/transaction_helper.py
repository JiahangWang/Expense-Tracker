# Description:
# This file contains shared validation and formatting helpers for transactions.
# It keeps transaction-input and transaction-display logic separate from the
# Tkinter layer.

from datetime import datetime


def validate_transaction_input(amount_raw, date_text, category, transaction_type, valid_types, valid_categories):
    """
    Validate and normalize one transaction form submission.
    """
    if not amount_raw or not date_text or not transaction_type or not category:
        raise ValueError("Amount, date, type, and category are required.")
    if transaction_type not in valid_types:
        raise ValueError("Please choose a valid transaction type.")
    if category not in valid_categories:
        raise ValueError("Please choose category from the dropdown.")

    try:
        amount = float(amount_raw)
    except ValueError as exc:
        raise ValueError("Amount must be a number.") from exc

    if amount <= 0:
        raise ValueError("Amount must be greater than 0.")

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Date must use YYYY-MM-DD format.") from exc

    return amount, date_text, category, transaction_type


def matches_period(date_text, selected_year, selected_month, selected_day="All"):
    """
    Check whether one date matches the selected period filters.
    """
    try:
        current_date = datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        return False

    if selected_year != "All" and current_date.year != int(selected_year):
        return False
    if selected_month != "All" and current_date.month != int(selected_month):
        return False
    if selected_day != "All" and current_date.day != int(selected_day):
        return False
    return True


def build_transaction_rows(transactions, selected_type, selected_year, selected_month, selected_day="All"):
    """
    Build filtered transaction rows for display in the output area.
    """
    rows = [
        {
            "id": transaction.transaction_id,
            "date": transaction.date,
            "category": transaction.category,
            "amount": transaction.amount,
            "type": transaction.get_type(),
        }
        for transaction in transactions
        if transaction.get_type() == selected_type
        and matches_period(transaction.date, selected_year, selected_month, selected_day)
    ]
    rows.sort(key=lambda row: (row["date"], row["id"]))
    return rows


def format_transaction_lines(rows):
    """
    Format transaction rows as a fixed-width text table.
    """
    header = f"{'ID':<6} {'Date':<12} {'Category':<16} {'Amount':>10}   {'Type':<8}"
    separator = "-" * len(header)
    lines = [header, separator]
    lines.extend(
        f"{row['id']:<6} {row['date']:<12} {row['category']:<16} {row['amount']:>10.2f}   {row['type']:<8}"
        for row in rows
    )
    return "\n".join(lines)
