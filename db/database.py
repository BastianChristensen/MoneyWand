import sqlite3

# Create Database

conn = sqlite3.connect("moneywand.db")

# Create cursor

# Stores one unique budget per month/year.

# CREATE TABLE budgets (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     year INTEGER NOT NULL,
#     month INTEGER NOT NULL,
#     total_budget REAL NOT NULL,
#     UNIQUE(year, month)
# );

# Customizable per month. You can link categories to a specific budget.

# CREATE TABLE categories (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     budget_id INTEGER NOT NULL,
#     name TEXT NOT NULL,
#     allocated_amount REAL,
#     FOREIGN KEY (budget_id) REFERENCES budgets(id)
# );

# CREATE TABLE expenses (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     category_id INTEGER NOT NULL,
#     date TEXT NOT NULL,
#     description TEXT,
#     amount REAL NOT NULL,
#     FOREIGN KEY (category_id) REFERENCES categories(id)
# );