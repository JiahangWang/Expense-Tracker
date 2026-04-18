import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config.app_config import TRANSACTION_TYPES
from core.analytics import category_summary, monthly_cashflow_summary, yearly_cashflow_summary
from core.charts import build_category_figure, build_monthly_trend_figure, build_yearly_trend_figure
from core.file_handler import load_transactions


def build_analytics(parent, user):
    frame = tk.Frame(parent, bg="#f1f5f9")

    tk.Label(frame, text="Analytics", font=("Helvetica", 16, "bold"),
             bg="#f1f5f9", fg="#1e293b").pack(anchor="w", padx=30, pady=(24, 12))

    # Controls bar
    controls = tk.Frame(frame, bg="#f1f5f9")
    controls.pack(anchor="w", padx=30, pady=(0, 10))

    # Chart mode
    mode_var = tk.StringVar(value="Category")
    for mode in ("Category", "Monthly Trend", "Yearly Trend"):
        tk.Radiobutton(controls, text=mode, variable=mode_var, value=mode,
                       bg="#f1f5f9", font=("Helvetica", 10),
                       command=lambda: _update_controls(mode_var, row2)).pack(side="left", padx=(0, 10))

    # Second row — dynamic controls
    row2 = tk.Frame(frame, bg="#f1f5f9")
    row2.pack(anchor="w", padx=30, pady=(0, 10))

    type_var  = tk.StringVar(value=TRANSACTION_TYPES[0])
    year_var  = tk.StringVar(value="All")
    month_var = tk.StringVar(value="All")
    chart_var = tk.StringVar(value="bar")

    years  = ["All"] + sorted({str(t.date[:4]) for t in load_transactions(user.data_file)}, reverse=True)
    months = ["All"] + [f"{m:02d}" for m in range(1, 13)]

    type_lbl  = tk.Label(row2, text="Type",  bg="#f1f5f9", font=("Helvetica", 10))
    type_menu = ttk.Combobox(row2, textvariable=type_var,  values=TRANSACTION_TYPES, state="readonly", width=10)
    year_lbl  = tk.Label(row2, text="Year",  bg="#f1f5f9", font=("Helvetica", 10))
    year_menu = ttk.Combobox(row2, textvariable=year_var,  values=years,  state="readonly", width=8)
    mon_lbl   = tk.Label(row2, text="Month", bg="#f1f5f9", font=("Helvetica", 10))
    mon_menu  = ttk.Combobox(row2, textvariable=month_var, values=months, state="readonly", width=8)
    chart_lbl = tk.Label(row2, text="Chart", bg="#f1f5f9", font=("Helvetica", 10))
    chart_menu = ttk.Combobox(row2, textvariable=chart_var, values=["bar", "pie"], state="readonly", width=7)

    _widgets = {
        "Category":       [type_lbl, type_menu, year_lbl, year_menu, mon_lbl, mon_menu, chart_lbl, chart_menu],
        "Monthly Trend":  [year_lbl, year_menu],
        "Yearly Trend":   [],
    }

    def _update_controls(mv, container):
        for w in container.winfo_children():
            w.pack_forget()
        for w in _widgets[mv.get()]:
            w.pack(side="left", padx=4)

    _update_controls(mode_var, row2)

    # Plot button
    canvas_holder = [None]

    def plot():
        mode = mode_var.get()
        transactions = load_transactions(user.data_file)

        try:
            if mode == "Category":
                summary = category_summary(user, type_var.get(),
                                           year_var.get(), month_var.get())
                if summary is None or summary.empty:
                    messagebox.showinfo("No Data", "No transactions match the selected filters.")
                    return
                fig = build_category_figure(type_var.get(), summary, chart_var.get())

            elif mode == "Monthly Trend":
                y = year_var.get()
                year = int(y) if y != "All" else None
                if year is None:
                    messagebox.showinfo("Select Year", "Please select a year for the monthly trend.")
                    return
                income, expense, net = monthly_cashflow_summary(transactions, year)
                fig = build_monthly_trend_figure(year, income, expense, net)

            else:
                years_data, inc, exp, net = yearly_cashflow_summary(transactions)
                if not years_data:
                    messagebox.showinfo("No Data", "No transactions found.")
                    return
                fig = build_yearly_trend_figure(years_data, inc, exp, net)

        except Exception as e:
            messagebox.showerror("Chart Error", str(e))
            return

        if canvas_holder[0]:
            canvas_holder[0].get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(fig, master=chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas_holder[0] = canvas

    tk.Button(frame, text="Plot", font=("Helvetica", 10),
              bg="#2563eb", fg="white", relief="flat", padx=14, pady=4,
              cursor="hand2", command=plot).pack(anchor="w", padx=30, pady=(0, 10))

    # Chart area
    chart_area = tk.Frame(frame, bg="#f1f5f9")
    chart_area.pack(fill="both", expand=True, padx=20)

    mode_var.trace_add("write", lambda *_: _update_controls(mode_var, row2))

    return frame
