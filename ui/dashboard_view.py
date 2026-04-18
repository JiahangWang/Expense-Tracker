"""
Author: Perfect
Date: 2026-04-16
Description: Dashboard view that summarizes balances and requests AI-generated insights.
"""

import threading
import tkinter as tk
from tkinter import messagebox

from core.ai_insights import get_insights
from core.file_handler import load_transactions
from core.tracker import ExpenseTracker


def build_dashboard(parent, user):
    """Build the dashboard frame and expose a refresh callback for navigation changes."""
    frame = tk.Frame(parent, bg="#f1f5f9")

    # The header contains the welcome text and the AI insight trigger button.
    header = tk.Frame(frame, bg="#f1f5f9")
    header.pack(fill="x", padx=30, pady=(28, 20))
    tk.Label(
        header,
        text=f"Welcome, {user.username.capitalize()}",
        font=("Helvetica", 16, "bold"),
        bg="#f1f5f9",
        fg="#1e293b",
    ).pack(side="left")
    insights_btn = tk.Button(
        header,
        text="Get Insights",
        font=("Helvetica", 10),
        bg="#7c3aed",
        fg="white",
        relief="flat",
        padx=10,
        pady=4,
        cursor="hand2",
        command=lambda: _fetch_insights(frame, user, insights_btn),
    )
    insights_btn.pack(side="right")

    # Summary cards display balance, total income, and total expense.
    cards_frame = tk.Frame(frame, bg="#f1f5f9")
    cards_frame.pack(padx=30)

    balance_var = tk.StringVar()
    income_var = tk.StringVar()
    expense_var = tk.StringVar()

    _card(cards_frame, "Balance", balance_var, "#2563eb").grid(row=0, column=0, padx=12)
    _card(cards_frame, "Total Income", income_var, "#16a34a").grid(row=0, column=1, padx=12)
    _card(cards_frame, "Total Expense", expense_var, "#dc2626").grid(row=0, column=2, padx=12)

    def refresh():
        """Reload transaction totals so the dashboard reflects the latest saved data."""
        tracker = ExpenseTracker()
        for transaction in load_transactions(user.data_file):
            tracker.add_transaction(transaction)

        all_transactions = tracker.get_all_transactions()
        income = sum(item.amount for item in all_transactions if item.get_type() == "Income")
        expense = sum(item.amount for item in all_transactions if item.get_type() == "Expense")
        income_var.set(f"${income:,.2f}")
        expense_var.set(f"${expense:,.2f}")
        balance_var.set(f"${tracker.get_balance():,.2f}")

    frame.refresh = refresh
    refresh()
    return frame


def _fetch_insights(parent, user, btn):
    """Request AI insights on a background thread to keep the UI responsive."""
    btn.config(state="disabled", text="Thinking...")

    def run():
        try:
            transactions = load_transactions(user.data_file)
            result = get_insights(transactions)
        except Exception as exc:
            result = None
            error = str(exc)
        else:
            error = None

        def done():
            """Restore the button state and show either the result dialog or an error."""
            btn.config(state="normal", text="Get Insights")
            if error:
                messagebox.showerror("Insights Error", error, parent=parent)
            else:
                _show_insights_dialog(parent, result)

        parent.after(0, done)

    threading.Thread(target=run, daemon=True).start()


def _show_insights_dialog(parent, text):
    """Display AI-generated spending insights in a read-only dialog window."""
    dialog = tk.Toplevel(parent)
    dialog.title("AI Insights")
    dialog.geometry("500x380")
    dialog.resizable(False, False)

    tk.Label(dialog, text="Spending Insights", font=("Helvetica", 13, "bold"), pady=14).pack()

    box = tk.Text(dialog, wrap="word", font=("Helvetica", 10), padx=16, pady=12, relief="flat", bg="#f8fafc")
    box.pack(fill="both", expand=True, padx=16, pady=(0, 12))
    box.insert("1.0", text)
    box.config(state="disabled")

    tk.Button(
        dialog,
        text="Close",
        command=dialog.destroy,
        bg="#1e293b",
        fg="white",
        relief="flat",
        padx=12,
        pady=5,
    ).pack(pady=(0, 14))


def _card(parent, title, value_var, color):
    """Create one reusable metric card used in the dashboard summary row."""
    card = tk.Frame(parent, bg="white", padx=28, pady=22, highlightbackground=color, highlightthickness=2)
    tk.Label(card, text=title, bg="white", fg="#64748b", font=("Helvetica", 10)).pack(anchor="w")
    tk.Label(card, textvariable=value_var, bg="white", fg=color, font=("Helvetica", 22, "bold")).pack(
        anchor="w",
        pady=(4, 0),
    )
    return card
