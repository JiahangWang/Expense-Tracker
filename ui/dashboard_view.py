import tkinter as tk

from core.file_handler import load_transactions
from core.tracker import ExpenseTracker


def build_dashboard(parent, user):
    tracker = ExpenseTracker()
    for t in load_transactions(user.data_file):
        tracker.add_transaction(t)

    total_income = sum(t.amount for t in tracker.get_all_transactions() if t.get_type() == "Income")
    total_expense = sum(t.amount for t in tracker.get_all_transactions() if t.get_type() == "Expense")
    balance = tracker.get_balance()

    frame = tk.Frame(parent, bg="#f1f5f9")

    tk.Label(frame, text=f"Welcome, {user.username.capitalize()} 👋", font=("Helvetica", 16, "bold"),
             bg="#f1f5f9", fg="#1e293b").pack(anchor="w", padx=30, pady=(28, 20))

    cards_frame = tk.Frame(frame, bg="#f1f5f9")
    cards_frame.pack(padx=30)

    _card(cards_frame, "Balance", balance, "#2563eb").grid(row=0, column=0, padx=12)
    _card(cards_frame, "Total Income", total_income, "#16a34a").grid(row=0, column=1, padx=12)
    _card(cards_frame, "Total Expense", total_expense, "#dc2626").grid(row=0, column=2, padx=12)

    return frame


def _card(parent, title, value, color):
    card = tk.Frame(parent, bg="white", padx=28, pady=22,
                    highlightbackground=color, highlightthickness=2)
    tk.Label(card, text=title, bg="white", fg="#64748b",
             font=("Helvetica", 10)).pack(anchor="w")
    tk.Label(card, text=f"${value:,.2f}", bg="white", fg=color,
             font=("Helvetica", 22, "bold")).pack(anchor="w", pady=(4, 0))
    return card
