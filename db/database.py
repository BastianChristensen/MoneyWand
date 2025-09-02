import sqlite3

# Create Database
conn = sqlite3.connect("moneywand.db")

# Cursor 
c = conn.cursor()

# Table for expenses 
c.execute("""CREATE TABLE if not exists expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    comment TEXT,
    budget_id INTEGER,
    FOREIGN KEY (budget_id) REFERENCES budgets(id)
)""")

# Table for budgets
c.execute("""CREATE TABLE if not exists budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INT,
    month TEXT
)""")