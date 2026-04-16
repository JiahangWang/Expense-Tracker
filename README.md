# Expense Tracker

## Project Description
Expense Tracker is a Python desktop app for recording and analyzing personal income and expenses.
It provides a Tkinter GUI, stores data in CSV, and supports category-based summaries and charts.

## Features
- Support user login and registration with per-user CSV data files
- Add Income and Expense transactions
- Track ID, amount, date, and category
- Delete a transaction by ID
- Show current balance
- Show transaction records filtered by Type + Year + Month + optional Day
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

### JSON Format
User account data uses this format:

```json
{
  "alice": {
    "password_hash": "hashed_password_value",
    "salt": "random_salt_value"
  },
  "bob": {
    "password_hash": "hashed_password_value",
    "salt": "random_salt_value"
  }
}
```
