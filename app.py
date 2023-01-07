import sqlite3

from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/")
def index():

    # Get disc info from database
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT name, plastic, run, image FROM inventory ORDER BY id DESC LIMIT 12;")
    rows = cursor.fetchall()

    # Organize query results into a list
    new_releases = []
    for row in rows:
        new_releases.append({"plastic": row[1], "name": row[0], "run": row[2], "image": row[3]})
    
    #Close database connection
    connection.close()

    return render_template("index.html", new_releases=new_releases)

@app.route("/search")
def search():

    # Get search value
    search = request.args.get("search")

    # Query database for search value
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT name, plastic, run, image FROM inventory WHERE name LIKE ?", [search])
    rows = cursor.fetchall()

    # Get number of results
    result_number = len(rows)

    # Organize query results into a list
    results = []
    for row in rows:
        results.append({"plastic": row[1], "name": row[0], "run": row[2], "image": row[3]})
    
    # Close database connection
    connection.close()

    return render_template("search.html", search=search, result_number=result_number, results=results)

@app.route("/item")
def item():

    # Get disc values
    item = request.args.get("item")

    # Query database for all discs with that name
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT plastic, run, weight, price, image FROM inventory WHERE name = ? ORDER BY id DESC", [item])
    rows = cursor.fetchall()

    # Organize results into a list
    items = []
    for row in rows:
        items.append({"plastic": row[0], "run": row[1], "weight": row[2], "price": row[3], "image": row[4]})

    # Close database connection
    connection.close()

    return render_template("item.html", items=items)