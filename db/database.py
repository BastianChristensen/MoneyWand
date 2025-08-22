import sqlite3

# Datatypes:
# NULL, does/doesnt exist.
# INT, whole numbers (ex: 1, 4, 2004)
# REAL, decimal numbers (ex: 1.4, 300.34)
# TEXT, text
# BLOB, as is

# Connect to database
conn = sqlite3.connect("data.db")

# Cursor
c = conn.cursor()

# Commit command
conn.commit()

# Close connection
conn.close()


