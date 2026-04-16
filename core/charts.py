# Description:
# This file provides helper functions to build matplotlib figures for the GUI.
# It includes category and cashflow trend charts for the Expense Tracker.

from matplotlib.figure import Figure


def build_category_figure(selected_type, summary, chart_type):
    """
    Create a category bar or pie chart figure.
    """
    figure = Figure(figsize=(7.2, 4.8), dpi=100)
    axis = figure.add_subplot(111)

    if chart_type == "bar":
        axis.bar(summary.index, summary.values, color="#3b82f6", edgecolor="#1d4ed8")
        axis.set_title(f"{selected_type} by Category")
        axis.set_xlabel("Category")
        axis.set_ylabel("Amount")
        axis.tick_params(axis="x", rotation=30)
    else:
        pie_colors = ["#3b82f6", "#22c55e", "#f97316", "#eab308", "#06b6d4", "#f43f5e", "#8b5cf6"]
        wedges, _, _ = axis.pie(
            summary.values,
            labels=None,
            autopct=lambda p: f"{p:.1f}%" if p >= 3 else "",
            startangle=90,
            colors=pie_colors[: len(summary.values)],
            pctdistance=0.7,
            textprops={"fontsize": 10},
        )
        axis.set_title(f"{selected_type} Category Share")
        axis.axis("equal")
        axis.legend(
            wedges,
            summary.index,
            title="Category",
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            frameon=False,
        )

    figure.tight_layout()
    if chart_type == "pie":
        figure.subplots_adjust(right=0.78)
    return figure


def build_monthly_trend_figure(year, monthly_income, monthly_expense, monthly_net):
    """
    Create the monthly cashflow trend figure for one selected year.
    """
    figure = Figure(figsize=(8.0, 5.0), dpi=100)
    axis = figure.add_subplot(111)

    months = list(range(1, 13))
    month_labels = [f"{month:02d}" for month in months]

    axis.plot(months, monthly_income, marker="o", linewidth=2.0, color="#16a34a", label="Income")
    axis.plot(months, monthly_expense, marker="o", linewidth=2.0, color="#dc2626", label="Expense")
    axis.plot(months, monthly_net, marker="o", linewidth=2.0, linestyle="--", color="#2563eb", label="Net")
    axis.set_title(f"Monthly Cashflow Trend ({year})")
    axis.set_xlabel("Month")
    axis.set_ylabel("Amount")
    axis.set_xticks(months)
    axis.set_xticklabels(month_labels)
    axis.grid(axis="y", linestyle="--", alpha=0.35)
    axis.legend(loc="best")

    figure.tight_layout()
    return figure


def build_yearly_trend_figure(years, yearly_income, yearly_expense, yearly_net):
    """
    Create the yearly cashflow trend figure across all available years.
    """
    figure = Figure(figsize=(8.0, 5.0), dpi=100)
    axis = figure.add_subplot(111)

    axis.plot(years, yearly_income, marker="o", linewidth=2.0, color="#16a34a", label="Income")
    axis.plot(years, yearly_expense, marker="o", linewidth=2.0, color="#dc2626", label="Expense")
    axis.plot(years, yearly_net, marker="o", linewidth=2.0, linestyle="--", color="#2563eb", label="Net")
    axis.set_title("Yearly Cashflow Trend")
    axis.set_xlabel("Year")
    axis.set_ylabel("Amount")
    axis.set_xticks(years)
    axis.grid(axis="y", linestyle="--", alpha=0.35)
    axis.legend(loc="best")

    figure.tight_layout()
    return figure
