import re
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
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


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for email
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")])
        rows = cursor.fetchall()

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Close database connection
        connection.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email")

        # Ensure first name was submitted
        if not request.form.get("first_name"):
            return apology("must provide first name")

        # Ensure last name was submitted
        elif not request.form.get("last_name"):
            return apology("must provide last name")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Ensure password is strong
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(password_pattern, request.form.get("password")):
            return apology("password must be at least 8 characters, must contain one uppercase letter, one lowercase letter, one number, and one special character")

        # Query database for email
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")])
        rows = cursor.fetchall()

        # Ensure email does not exist
        if len(rows) != 0:
            return apology("username already exists")

        # Add user to database
        email = request.form.get("email")
        hash = generate_password_hash(request.form.get("password"))
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        cursor.execute("INSERT INTO users (email, password, first_name, last_name) VALUES(?, ?, ?, ?)", (email, hash, first_name, last_name))
        connection.commit()

        # Close database connection
        connection.close()

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


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

    # Get all plastic types
    cursor.execute("SELECT DISTINCT plastic FROM inventory WHERE name = ?", [item])
    rows = cursor.fetchall()
    plastics = []
    for row in rows:
        plastics.append(row[0])

    # Get all runs
    cursor.execute("SELECT DISTINCT run FROM inventory WHERE name = ?", [item])
    rows = cursor.fetchall()
    runs = []
    for row in rows:
        runs.append(row[0])
    
    # Get item title
    cursor.execute("SELECT brand FROM inventory WHERE name = ?", [item])
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
    cursor.execute("SELECT max(name), brand, speed, glide, turn, fade, image FROM inventory WHERE type = ? GROUP BY name", [type])
    rows = cursor.fetchall()

    # Organize results into a list
    results = []
    for row in rows:
        results.append({"brand": row[1], "name": row[0], "speed": row[2], "glide": row[3], "turn": row[4], "fade": row[5], "image": row[6]})
    
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
    cursor.execute("SELECT max(name), speed, glide, turn, fade, image FROM inventory WHERE brand = ? GROUP BY name", [brand])
    rows = cursor.fetchall()

    # Organize results into a list
    results = []
    for row in rows:
        results.append({"name": row[0], "speed": row[1], "glide": row[2], "turn": row[3], "fade": row[4], "image": row[5]})
    
    # Close database connection
    connection.close()

    return render_template("search-by-brand.html", brand=brand, results=results)