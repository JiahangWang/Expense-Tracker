# Expense Tracker

## Project Description
Expense Tracker is a Python desktop app for recording and analyzing personal income and expenses.
It provides a Tkinter GUI, stores data in CSV, and supports category-based summaries and charts.

## Features
- Add Income and Expense transactions
- Track amount, date, and category
- Show current balance
- Show transactions filtered by Type + Year + Month
- Show category summary filtered by Type + Year + Month
- Visualize category totals with:
  - Bar chart
  - Pie chart
- Persist data to data/data.csv

## Tech Stack
- Python 3.x
- tkinter (GUI)
- pandas (data analysis)
- matplotlib (charts)
- CSV file storage

## Project Structure
```text
tracker/
|-- main.py               # Thin application entrypoint
|-- README.md             # Project documentation
|-- .gitignore
|-- config/
|   `-- app_config.py     # Shared constants and file paths
|-- core/
|   |-- analytics.py      # Data analysis helpers
|   |-- charts.py         # Matplotlib figure builders
|   |-- file_handler.py   # CSV save/load functions
|   |-- tracker.py        # Core tracker logic
|   `-- transaction.py    # Transaction / Expense / Income classes
|-- data/
|   `-- data.csv          # Local transaction dataset
`-- ui/
    `-- main_window.py    # Tkinter GUI and interaction flow
```

## Requirements
Install dependencies:

```bash
pip install pandas matplotlib
```

## How to Run
From the project directory:

```bash
python main.py
```

## CSV Format
`data/data.csv` uses this format:

```csv
amount,date,category,type
50,2026-04-01,food,Expense
1000,2026-04-01,salary,Income
```

## Notes
- Date format is expected as YYYY-MM-DD.
- The app reads existing transactions from `data/data.csv` on startup.
- After adding a transaction, data is saved immediately to `data/data.csv`.
