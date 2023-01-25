import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask import Flask, redirect, request, render_template, url_for

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
    cursor.execute("SELECT max(mold), brand, speed, glide, turn, fade, image FROM inventory WHERE type != 'Accessory' AND type != 'Apparel' GROUP BY mold;")
    rows = cursor.fetchall()
    disc_inventory = []
    for row in rows:
        disc_inventory.append({"mold": row[0], "brand": row[1], "speed": row[2], "glide": row[3], "turn": row[4], "fade": row[5], "image": row[6]})
    rows.clear()

    # Get new release disc info from database
    cursor.execute("SELECT DISTINCT mold, plastic, run, image FROM inventory WHERE type != 'Accessory' AND type != 'Apparel' ORDER BY id DESC LIMIT 24;")
    rows = cursor.fetchall()
    new_releases = []
    for row in rows:
        new_releases.append({"plastic": row[1], "mold": row[0], "run": row[2], "image": row[3]})
    rows.clear()
    
    # Get new apparel from database
    cursor.execute("SELECT DISTINCT brand, mold, image FROM inventory WHERE type = 'Apparel' ORDER BY id DESC LIMIT 12;")
    rows = cursor.fetchall()
    new_apparel = []
    for row in rows:
        new_apparel.append({"brand": row[0], "mold": row[1], "image": row[2]})
    rows.clear()

    # Get new accessories from database
    cursor.execute("SELECT DISTINCT brand, mold, image FROM inventory WHERE type = 'Accessory' ORDER BY id DESC LIMIT 12;")
    rows = cursor.fetchall()
    new_accessories = []
    for row in rows:
        new_accessories.append({"brand": row[0], "mold": row[1], "image": row[2]})
    rows.clear()
    
    #Close database connection
    connection.close()

    return render_template("index.html", disc_inventory=disc_inventory, new_releases=new_releases, new_apparel=new_apparel, new_accessories=new_accessories)


@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == "GET":
        # Get search values
        search = request.args.get("search")

        # Query database for search value
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT brand, mold, plastic, run, speed, glide, turn, fade, image FROM inventory WHERE mold LIKE ? OR run LIKE ? OR brand LIKE ? OR type LIKE ? ORDER BY mold", (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
        rows = cursor.fetchall()

        # Get number of results
        result_number = len(rows)

        # Organize query results into a list
        results = []
        for row in rows:
            results.append({"brand": row[0], "plastic": row[2], "mold": row[1], "run": row[3], "speed": row[4], "glide": row[5], "turn": row[6], "fade": row[7], "image": row[8]})
        
        # Close database connection
        connection.close()

        return render_template("search.html", search=search, result_number=result_number, results=results)
    
    if request.method == "POST":
        # Get flight numbers
        speed = int(request.form.get("speed"))
        glide = int(request.form.get("glide"))
        turn = int(request.form.get("turn"))
        fade = int(request.form.get("fade"))

        # Get value to display in heading
        if speed == 0:
            speed_heading = "-"
        else:
            speed_heading = speed
        if glide == 0:
            glide_heading = "-"
        else:
            glide_heading = glide
        if turn == -6:
            turn_heading = "-"
        else:
            turn_heading = turn
        if fade == -1:
            fade_heading = "-"
        else:
            fade_heading = fade
        search = f"{speed_heading} | {glide_heading} | {turn_heading} | {fade_heading}"

        # Change values to SQL queries
        if speed == 0:
            speed_query = "SELECT DISTINCT mold FROM inventory WHERE type != 'Accessory' AND type != 'Apparel'"
        else:
            speed_query = f"SELECT DISTINCT mold FROM inventory WHERE type != 'Accessory' AND type != 'Apparel' AND speed = {speed}"
        if glide == 0:
            glide_query = "SELECT DISTINCT mold FROM inventory WHERE type != 'Accessory' AND type != 'Apparel'"
        else:
            glide_query = f"SELECT DISTINCT mold FROM inventory WHERE type != 'Accessory' AND type != 'Apparel' AND glide = {glide}"
        if turn == -6:
            turn_query = "SELECT DISTINCT mold FROM inventory WHERE type != 'Accessory' AND type != 'Apparel'"
        else:
            turn_query = f"SELECT DISTINCT mold FROM inventory WHERE type != 'Accessory' AND type != 'Apparel' AND turn = {turn}"
        if fade == -1:
            fade_query = "SELECT max(mold), brand, speed, glide, turn, fade, image FROM inventory WHERE type != 'Accessory' AND type != 'Apparel'"
        else:
            fade_query = f"SELECT max(mold), brand, speed, glide, turn, fade, image FROM inventory WHERE type != 'Accessory' AND type != 'Apparel' AND fade = {fade}"

        # Query database for molds matching flight numbers
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        query = f"{fade_query} AND mold IN ({turn_query} AND mold IN ({glide_query} AND mold IN ({speed_query}))) GROUP BY mold"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Get number of results
        result_number = len(rows)

        # Organize query results into a list
        results = []
        for row in rows:
            results.append({"brand": row[1], "mold": row[0], "speed": row[2], "glide": row[3], "turn": row[4], "fade": row[5], "image": row[6]})     

        return render_template("search.html", search=search, result_number=result_number, results=results)


@app.route("/search-by-type")
def search_by_type():

    # Get type
    type = request.args.get("type")

    # Query database for all distance drivers
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    if type == "All Discs":
        cursor.execute("SELECT max(mold), brand, plastic, run, speed, glide, turn, fade, image FROM inventory WHERE type != 'Apparel' AND type != 'Accessory' GROUP BY mold, plastic, run")
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({"brand": row[1], "mold": row[0], "plastic": row[2], "run": row[3], "speed": row[4], "glide": row[5], "turn": row[6], "fade": row[7], "image": row[8]})
    else:
        cursor.execute("SELECT max(mold), brand, speed, glide, turn, fade, image FROM inventory WHERE type = ? GROUP BY mold", [type])
        rows = cursor.fetchall()
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
    cursor.execute("SELECT max(mold), speed, glide, turn, fade, image FROM inventory WHERE brand = ? AND type != 'Apparel' AND type != 'Accessory' GROUP BY mold", [brand])
    rows = cursor.fetchall()

    # Organize results into a list
    results = []
    for row in rows:
        results.append({"mold": row[0], "speed": row[1], "glide": row[2], "turn": row[3], "fade": row[4], "image": row[5]})
    
    # Close database connection
    connection.close()

    return render_template("search-by-brand.html", brand=brand, results=results)


@app.route("/item")
def item():

    # Get disc values
    item = request.args.get("item")

    # Query database for all discs with that name
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, brand, plastic, run, weight, type, speed, glide, turn, fade, price, image FROM inventory WHERE mold = ? ORDER BY id DESC", [item])
    rows = cursor.fetchall()

    # Organize results into a list
    items = []
    for row in rows:
        items.append({"id": row[0], "brand": row[1], "plastic": row[2], "run": row[3], "weight": row[4], "type": row[5], "speed": row[6], "glide": row[7], "turn": row[8], "fade": row[9], "price": row[10], "image": row[11]})

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

    # Get stock item image
    cursor.execute("SELECT image FROM inventory WHERE mold = ? AND run = 'Stock'", [item])
    row = cursor.fetchone()
    if row is None:
        cursor.execute("SELECT image FROM inventory WHERE mold = ?", [item])
        row = cursor.fetchone()
    thumbnail = row[0]

    # Close database connection
    connection.close()

    return render_template("item.html", items=items, plastics=plastics, runs=runs, title=title, thumbnail=thumbnail)


@app.route("/cart", methods=["GET", "POST"])
def cart():

    # Add item to cart
    if request.method == "POST":

        if not session.get("cart"):
            session["cart"] = []
        item_id = request.form.get("id")

        # Get item info from database
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, brand, mold, plastic, run, weight, price, image FROM inventory WHERE id = ?", [item_id])
        row = cursor.fetchone()
        item = {"id": row[0], "brand": row[1], "mold": row[2], "plastic": row[3], "run": row[4], "weight": row[5], "price": row[6], "image": row[7]}
        session["cart"].append(item)
        connection.close()

        return redirect(url_for("cart"))
    
    if request.method == "GET":

        if not session.get("cart"):
            cart = []
        else:
            cart = session.get("cart", None)

        # Get total price
        total = 0
        for item in cart:
            total += item["price"]
        total = round(total, 2)
        
        return render_template("cart.html", cart=cart, total=total)


@app.route("/remove", methods=["POST"])
def remove():

    item_id = int(request.form.get("id"))

    # Remove item from cart
    cart = []
    for i in range(len(session["cart"])):
        if session["cart"][i]["id"] == item_id:
            del session["cart"][i]
            break

    return redirect(url_for("cart"))


@app.route("/checkout", methods=["POST"])
def checkout():

    # Empty cart
    session.clear()
    flash('Your order is on its way!')

    return redirect(url_for("index"))