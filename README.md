# Expense Tracker

## 📌 Project Description
The Expense Tracker is a Python application that allows users to record and manage income and expenses through a graphical user interface. The system supports data storage using CSV files and provides basic data analysis using pandas.

---

## 🚀 Features
- Add income and expense transactions
- Categorize transactions
- View current balance
- Store and load data from CSV files
- Basic data analysis (e.g., category summary)

---

## 🧰 Technology Stack
- Python 3.12  
- tkinter (GUI)  
- pandas (Data Analysis)  
- CSV File I/O  
- pytest  
- GitHub  

---

## 📁 Project Structure
expense_tracker_project/
│
├── main.py # GUI (main program)
│
├── transaction.py # Transaction, Expense, Income classes
├── tracker.py # Core logic (manage transactions)
├── file_handler.py # CSV read/write functions
├── analytics.py # Data analysis using pandas
│
├── data.csv # Stored transaction data
│
├── test_tracker.py # Unit tests (pytest)
│
└── README.md # Project documentation
---

## ▶️ How to Run
1. Make sure Python 3.12 is installed
2. Install required libraries: ```pip install pandas```
3. Run the program:
---
## 🧪 Testing
To run tests:
pytest test_tracker.py
---
## 📊 Example Data Format (data.csv)
amount,date,category,type
50,2026-04-01,Food,Expense
1000,2026-04-01,Salary,Income
---
## 📝 Notes
- The application uses a simple GUI built with tkinter.
- Data is stored locally in a CSV file.
- The system is designed to be easily extended with additional features.






