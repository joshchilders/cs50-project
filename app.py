import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():

    # Load each unique mold in inventory for search-by-flight section
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT max(mold), brand, speed, glide, turn, fade, image FROM inventory GROUP BY mold")
    rows = cursor.fetchall()
    disc_inventory = []
    for row in rows:
        disc_inventory.append({"mold": row[0], "brand": row[1], "speed": row[2], "glide": row[3], "turn": row[4], "fade": row[5], "image": row[6]})

    # Get new release disc info from database
    cursor.execute("SELECT DISTINCT mold, plastic, run, image FROM inventory ORDER BY id DESC LIMIT 12;")
    rows = cursor.fetchall()

    # Organize query results into a list
    new_releases = []
    for row in rows:
        new_releases.append({"plastic": row[1], "mold": row[0], "run": row[2], "image": row[3]})
    
    #Close database connection
    connection.close()

    return render_template("index.html", disc_inventory=disc_inventory, new_releases=new_releases)


@app.route("/search")
def search():

    # Get search value
    search = request.args.get("search")

    # Query database for search value
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT mold, plastic, run, image FROM inventory WHERE mold LIKE ?", [search])
    rows = cursor.fetchall()

    # Get number of results
    result_number = len(rows)

    # Organize query results into a list
    results = []
    for row in rows:
        results.append({"plastic": row[1], "mold": row[0], "run": row[2], "image": row[3]})
    
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
    cursor.execute("SELECT brand, plastic, run, weight, type, speed, glide, turn, fade, price, image FROM inventory WHERE mold = ? ORDER BY id DESC", [item])
    rows = cursor.fetchall()

    # Organize results into a list
    items = []
    for row in rows:
        items.append({"brand": row[0], "plastic": row[1], "run": row[2], "weight": row[3], "type": row[4], "speed": row[5], "glide": row[6], "turn": row[7], "fade": row[8], "price": row[9], "image": row[10]})

    # Get all plastic types
    cursor.execute("SELECT DISTINCT plastic FROM inventory WHERE mold = ?", [item])
    rows = cursor.fetchall()
    plastics = []
    for row in rows:
        plastics.append(row[0])

    # Get all runs associated with each plastic
    runs = {}
    for plastic in plastics:
        cursor.execute("SELECT DISTINCT run FROM inventory WHERE mold = ? AND plastic = ?", (item, plastic))
        rows = cursor.fetchall()
        temp = []
        for row in rows:
            temp.append(row[0])
            runs[plastic] = temp
    
    # Get item title
    cursor.execute("SELECT brand FROM inventory WHERE mold = ?", [item])
    row = cursor.fetchone()
    title = row[0] + " " + item

    # Close database connection
    connection.close()

    return render_template("item.html", items=items, plastics=plastics, runs=runs, title=title)


@app.route("/search-by-type")
def search_by_type():

    # Get type
    type = request.args.get("type")

    # Query database for all distance drivers
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT max(mold), brand, speed, glide, turn, fade, image FROM inventory WHERE type = ? GROUP BY mold", [type])
    rows = cursor.fetchall()

    # Organize results into a list
    results = []
    for row in rows:
        results.append({"brand": row[1], "mold": row[0], "speed": row[2], "glide": row[3], "turn": row[4], "fade": row[5], "image": row[6]})
    
    # Close database connection
    connection.close()

    return render_template("search-by-type.html", type=type, results=results)


@app.route("/search-by-brand")
def search_by_brand():

    # Get type
    brand = request.args.get("brand")

    # Query database for all distance drivers
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT max(mold), speed, glide, turn, fade, image FROM inventory WHERE brand = ? GROUP BY mold", [brand])
    rows = cursor.fetchall()

    # Organize results into a list
    results = []
    for row in rows:
        results.append({"mold": row[0], "speed": row[1], "glide": row[2], "turn": row[3], "fade": row[4], "image": row[5]})
    
    # Close database connection
    connection.close()

    return render_template("search-by-brand.html", brand=brand, results=results)


@app.route("/cart")
def cart():


    return render_template("cart.html")