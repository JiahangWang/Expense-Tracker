# Expense Tracker

## Project Description
Expense Tracker is a Python desktop app for recording and analyzing personal income and expenses.
It provides a Tkinter GUI, stores data in CSV, and supports category-based summaries and charts.

## Features
- Add Income and Expense transactions
- Track ID, amount, date, and category
- Delete a transaction by ID
- Show current balance
- Show transactions filtered by Type + Year + Month
- Show daily records filtered by Type + Year + Month + Day
- Show category summary filtered by Type + Year + Month
- Show category visuals with:
  - Category bar chart
  - Category pie chart
- Show cashflow trend with:
  - Year Trend across all available years
  - Month Trend for one selected year
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
|-- main.py               # App entry
|-- README.md             # Docs
|-- .gitignore
|-- config/
|   `-- app_config.py     # Constants
|-- core/
|   |-- analytics.py      # Analysis
|   |-- charts.py         # Charts
|   |-- file_handler.py   # CSV I/O
|   |-- tracker.py        # Tracker logic
|   `-- transaction.py    # Transaction models
|-- data/
|   `-- data.csv          # Sample data
`-- ui/
    `-- main_window.py    # Tkinter UI
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
id,amount,date,category,type
1,50,2026-04-01,food,Expense
2,1000,2026-04-01,salary,Income
```
