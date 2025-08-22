import sqlite3

# Datatypes:
# NULL, does/doesnt exist.
# INT, whole numbers (ex: 1, 4, 2004)
# REAL, decimal numbers (ex: 1.4, 300.34)
# TEXT, text
# BLOB, as is

# Connect to database
def create_database():
    conn = sqlite3.connect("data.db")

    # Cursor
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            comment TEXT
        )      
            """)

    # Commit command
    conn.commit()

    # Close connection
    conn.close()


