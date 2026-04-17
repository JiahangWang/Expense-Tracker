import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from config.app_config import INCOME_CATEGORIES, EXPENSE_CATEGORIES, TRANSACTION_TYPES
from core.file_handler import load_transactions, save_transactions
from core.tracker import ExpenseTracker
from core.transaction import Income, Expense
from core.transaction_helper import validate_transaction_input


def build_transactions(parent, user):
    tracker = ExpenseTracker()
    for t in load_transactions(user.data_file):
        tracker.add_transaction(t)

    frame = tk.Frame(parent, bg="#f1f5f9")

    # Header row
    header = tk.Frame(frame, bg="#f1f5f9")
    header.pack(fill="x", padx=30, pady=(24, 10))
    tk.Label(header, text="Transactions", font=("Helvetica", 16, "bold"),
             bg="#f1f5f9", fg="#1e293b").pack(side="left")
    tk.Button(header, text="+ Add", font=("Helvetica", 10),
              bg="#2563eb", fg="white", relief="flat", padx=10, pady=4, cursor="hand2",
              command=lambda: _open_add_dialog(frame, tracker, user, tree)).pack(side="right")
    tk.Button(header, text="Delete", font=("Helvetica", 10),
              bg="#dc2626", fg="white", relief="flat", padx=10, pady=4, cursor="hand2",
              command=lambda: _delete_selected(tracker, user, tree)).pack(side="right", padx=(0, 8))

    # Table
    cols = ("ID", "Date", "Category", "Amount", "Type")
    tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
    for col in cols:
        tree.heading(col, text=col)
    tree.column("ID", width=50, anchor="center")
    tree.column("Date", width=100, anchor="center")
    tree.column("Category", width=140)
    tree.column("Amount", width=100, anchor="e")
    tree.column("Type", width=90, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=(0, 20))
    scrollbar.pack(side="left", fill="y", pady=(0, 20))

    _refresh(tree, tracker)
    return frame


def _refresh(tree, tracker):
    tree.delete(*tree.get_children())
    for t in sorted(tracker.get_all_transactions(), key=lambda x: x.date, reverse=True):
        tag = "income" if t.get_type() == "Income" else "expense"
        tree.insert("", "end", iid=t.transaction_id,
                    values=(t.transaction_id, t.date, t.category, f"${t.amount:,.2f}", t.get_type()),
                    tags=(tag,))
    tree.tag_configure("income", foreground="#16a34a")
    tree.tag_configure("expense", foreground="#dc2626")


def _delete_selected(tracker, user, tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a transaction to delete.")
        return
    transaction_id = int(selected[0])
    tracker.delete_transaction_by_id(transaction_id)
    save_transactions(user.data_file, tracker.get_all_transactions())
    _refresh(tree, tracker)


def _open_add_dialog(parent, tracker, user, tree):
    dialog = tk.Toplevel(parent)
    dialog.title("Add Transaction")
    dialog.resizable(False, False)
    dialog.grab_set()

    f = tk.Frame(dialog, padx=24, pady=20)
    f.pack()

    # Type
    tk.Label(f, text="Type").grid(row=0, column=0, sticky="w", pady=4)
    type_var = tk.StringVar(value=TRANSACTION_TYPES[0])
    type_menu = ttk.Combobox(f, textvariable=type_var, values=TRANSACTION_TYPES,
                             state="readonly", width=20)
    type_menu.grid(row=0, column=1, pady=4)

    # Category
    tk.Label(f, text="Category").grid(row=1, column=0, sticky="w", pady=4)
    cat_var = tk.StringVar()
    cat_menu = ttk.Combobox(f, textvariable=cat_var, state="readonly", width=20)
    cat_menu.grid(row=1, column=1, pady=4)

    def update_categories(*_):
        cats = INCOME_CATEGORIES if type_var.get() == "Income" else EXPENSE_CATEGORIES
        cat_menu["values"] = cats
        cat_var.set(cats[0])

    type_var.trace_add("write", update_categories)
    update_categories()

    # Amount
    tk.Label(f, text="Amount").grid(row=2, column=0, sticky="w", pady=4)
    amount_entry = tk.Entry(f, width=22)
    amount_entry.grid(row=2, column=1, pady=4)

    # Date
    tk.Label(f, text="Date (YYYY-MM-DD)").grid(row=3, column=0, sticky="w", pady=4)
    date_entry = tk.Entry(f, width=22)
    date_entry.insert(0, str(date.today()))
    date_entry.grid(row=3, column=1, pady=4)

    def submit():
        valid_cats = INCOME_CATEGORIES if type_var.get() == "Income" else EXPENSE_CATEGORIES
        try:
            amount, date_text, category, t_type = validate_transaction_input(
                amount_entry.get(), date_entry.get(),
                cat_var.get(), type_var.get(),
                TRANSACTION_TYPES, valid_cats,
            )
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e), parent=dialog)
            return

        tid = tracker.get_next_transaction_id()
        transaction = Income(tid, amount, date_text, category) if t_type == "Income" \
            else Expense(tid, amount, date_text, category)
        tracker.add_transaction(transaction)
        save_transactions(user.data_file, tracker.get_all_transactions())
        _refresh(tree, tracker)
        dialog.destroy()

    tk.Button(f, text="Save", bg="#2563eb", fg="white", relief="flat",
              padx=12, pady=5, command=submit).grid(row=4, column=1, sticky="e", pady=(14, 0))
