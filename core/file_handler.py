# Description:
# This file provides functions to save and load transaction data using CSV files.
# It keeps user transaction data persistent between application sessions.

import csv

from core.transaction import Expense, Income


def save_transactions(file_path, transactions):
    """
    Save a list of transactions to a CSV file.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "amount", "date", "category", "type"])
        for transaction in transactions:
            writer.writerow(
                [
                    transaction.transaction_id,
                    transaction.amount,
                    transaction.date,
                    transaction.category,
                    transaction.get_type(),
                ]
            )


def load_transactions(file_path):
    """
    Load transactions from a CSV file and recreate transaction objects.
    """
    transactions = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            next_generated_id = 1

            for row in reader:
                transaction_id_raw = row.get("id", "").strip()
                if transaction_id_raw:
                    transaction_id = int(transaction_id_raw)
                    next_generated_id = max(next_generated_id, transaction_id + 1)
                else:
                    transaction_id = next_generated_id
                    next_generated_id += 1

                amount = float(row["amount"])
                date = row["date"]
                category = row["category"]
                transaction_type = row["type"]

                if transaction_type == "Expense":
                    transaction = Expense(transaction_id, amount, date, category)
                elif transaction_type == "Income":
                    transaction = Income(transaction_id, amount, date, category)
                else:
                    continue

                transactions.append(transaction)
    except FileNotFoundError:
        return []

    return transactions
