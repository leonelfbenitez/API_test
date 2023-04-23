import sqlite3

# open connection to database
conn = sqlite3.connect("database.db")
cur = conn.cursor()

# retrieve all records from inventory table
cur.execute("SELECT * FROM inventory;")
rows = cur.fetchall()

print(rows)

# close connection to database
cur.close()
conn.close()
