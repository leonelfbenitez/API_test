import sqlite3
import os.path
from flask import jsonify


if not os.path.exists("database.db"):

	# open connection to database
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()

	# create inventory table
	conn.execute("""CREATE TABLE inventory(
		bookId INTEGER PRIMARY KEY, 
		name TEXT, 
		description TEXT, 
		category VARCHAR(50), 
		price REAL, 
		stock INTEGER
		);""")

	# commit changes and close connection to the database
	conn.commit()
	cursor.close()
	conn.close()
		
	# insert mockup data
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()

	cursor.execute("""INSERT INTO inventory (name, description, category, price, stock) VALUES 
	('To Kill a Mockingbird', 'A novel by Harper Lee', 'Fiction', 10.99, 50), 
	('The Great Gatsby', 'A novel by F. Scott Fitzgerald', 'Fiction', 12.99, 25), 
	('1984', 'A dystopian novel by George Orwell', 'Fiction', 9.99, 35), 
	('The Art of War', 'A book on military strategy by Sun Tzu', 'Non-Fiction', 8.99, 40), 
	('The Elements of Style', 'A guide to writing by William Strunk Jr. and E.B. White', 'Non-Fiction', 6.99, 30), 
	('The Catcher in the Rye', 'A novel by J.D. Salinger', 'Fiction', 11.99, 20);""")
		
	conn.commit()
	cursor.close()
	conn.close()	

else:
	conn = sqlite3.connect("database.db")
	conn.close()
