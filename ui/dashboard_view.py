import threading
import tkinter as tk
from tkinter import messagebox

from core.ai_insights import get_insights
from core.file_handler import load_transactions
from core.tracker import ExpenseTracker


def build_dashboard(parent, user):
    frame = tk.Frame(parent, bg="#f1f5f9")

    # Header row
    header = tk.Frame(frame, bg="#f1f5f9")
    header.pack(fill="x", padx=30, pady=(28, 20))
    tk.Label(header, text=f"Welcome, {user.username.capitalize()} 👋",
             font=("Helvetica", 16, "bold"), bg="#f1f5f9", fg="#1e293b").pack(side="left")
    insights_btn = tk.Button(header, text="✨ Get Insights", font=("Helvetica", 10),
                             bg="#7c3aed", fg="white", relief="flat", padx=10, pady=4,
                             cursor="hand2", command=lambda: _fetch_insights(frame, user, insights_btn))
    insights_btn.pack(side="right")

    # Cards
    cards_frame = tk.Frame(frame, bg="#f1f5f9")
    cards_frame.pack(padx=30)

    balance_var = tk.StringVar()
    income_var  = tk.StringVar()
    expense_var = tk.StringVar()

    _card(cards_frame, "Balance",       balance_var, "#2563eb").grid(row=0, column=0, padx=12)
    _card(cards_frame, "Total Income",  income_var,  "#16a34a").grid(row=0, column=1, padx=12)
    _card(cards_frame, "Total Expense", expense_var, "#dc2626").grid(row=0, column=2, padx=12)

    def refresh():
        tracker = ExpenseTracker()
        for t in load_transactions(user.data_file):
            tracker.add_transaction(t)
        all_t = tracker.get_all_transactions()
        income  = sum(t.amount for t in all_t if t.get_type() == "Income")
        expense = sum(t.amount for t in all_t if t.get_type() == "Expense")
        income_var.set(f"${income:,.2f}")
        expense_var.set(f"${expense:,.2f}")
        balance_var.set(f"${tracker.get_balance():,.2f}")

    frame.refresh = refresh
    refresh()
    return frame


def _fetch_insights(parent, user, btn):
    btn.config(state="disabled", text="Thinking...")

    def run():
        try:
            transactions = load_transactions(user.data_file)
            result = get_insights(transactions)
        except Exception as e:
            result = None
            error = str(e)
        else:
            error = None

        def done():
            btn.config(state="normal", text="✨ Get Insights")
            if error:
                messagebox.showerror("Insights Error", error, parent=parent)
            else:
                _show_insights_dialog(parent, result)

        parent.after(0, done)

    threading.Thread(target=run, daemon=True).start()


def _show_insights_dialog(parent, text):
    dialog = tk.Toplevel(parent)
    dialog.title("AI Insights")
    dialog.geometry("500x380")
    dialog.resizable(False, False)

    tk.Label(dialog, text="✨ Spending Insights", font=("Helvetica", 13, "bold"),
             pady=14).pack()

    box = tk.Text(dialog, wrap="word", font=("Helvetica", 10),
                  padx=16, pady=12, relief="flat", bg="#f8fafc")
    box.pack(fill="both", expand=True, padx=16, pady=(0, 12))
    box.insert("1.0", text)
    box.config(state="disabled")

    tk.Button(dialog, text="Close", command=dialog.destroy,
              bg="#1e293b", fg="white", relief="flat", padx=12, pady=5).pack(pady=(0, 14))


def _card(parent, title, value_var, color):
    card = tk.Frame(parent, bg="white", padx=28, pady=22,
                    highlightbackground=color, highlightthickness=2)
    tk.Label(card, text=title, bg="white", fg="#64748b",
             font=("Helvetica", 10)).pack(anchor="w")
    tk.Label(card, textvariable=value_var, bg="white", fg=color,
             font=("Helvetica", 22, "bold")).pack(anchor="w", pady=(4, 0))
    return card
