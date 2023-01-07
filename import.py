import csv
import sqlite3

# Connect to database
connection = sqlite3.connect("inventory.db")

# Create cursor object to execute SQL queries
cursor = connection.cursor()

# Open csv file
file = open("inventory.csv")

# Read contents of file
contents = csv.reader(file)

# SQL query
insert_records = "INSERT INTO inventory (brand, name, plastic, run, weight, type, speed, glide, turn, fade, price, sold) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)"

#Import contents into database
cursor.executemany(insert_records, contents)

# SQL query to verify data has been successfully imported
select_all = "SELECT * FROM inventory"
rows = cursor.execute(select_all).fetchall()

# Output to console screen
for r in rows:
    print(r)

# Commit the changes
connection.commit()

# Close database connection
connection.close()