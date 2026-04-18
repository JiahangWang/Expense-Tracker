# Expense Tracker

## Project Description
Expense Tracker is a Python desktop app for recording and analyzing personal income and expenses.
It provides a Tkinter GUI, stores users and transactions in MySQL, and supports category-based summaries, charts, and AI-generated insights.

## Features
- Support user login and registration
- Store user accounts and transactions in MySQL
- Add Income and Expense transactions
- Track ID, amount, date, and category
- Delete a transaction by ID
- Show current balance
- Show transaction records in a tabular view
- Show category summary filtered by Type + Year + Month
- Show category visuals with:
  - Category bar chart
  - Category pie chart
- Show cashflow trend with:
  - Year Trend across all available years
  - Month Trend for one selected year
- Generate AI insights from transaction history
- Automatically import legacy `data/users.json` and per-user CSV files into MySQL when the database is empty

## Tech Stack
- Python 3.x
- tkinter (GUI)
- MySQL
- pandas (data analysis)
- matplotlib (charts)
- python-dotenv (load environment variables from `.env`)
- google-generativeai (AI insights)
- mysql-connector-python (database driver)

## Requirements
Install dependencies:

```bash
pip install -r requirements.txt
```

Notes:
- `tkinter` is part of the Python standard library in many distributions, but some systems may require installing Tk separately.
- You need a running MySQL server before starting the app.
- The app creates the target database and tables automatically if your MySQL account has permission.

## Environment Setup
Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=expense_tracker
```

## How to Run
From the project directory:

```bash
python main.py
```

If `python` points to a different interpreter on your machine, use the interpreter from your active environment instead.

## Database Schema
The application creates these tables automatically:

### `users`
- `id`
- `username`
- `password_hash`
- `salt`
- `created_at`

### `transactions`
- `record_id`
- `user_id`
- `transaction_id`
- `amount`
- `transaction_date`
- `category`
- `transaction_type`
- `created_at`
