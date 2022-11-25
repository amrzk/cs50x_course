import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///expenses.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # retrieving user's history

    return render_template("index.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Look up the user's entries
    history = db.execute("SELECT amount, description, date, categories.category FROM entries INNER JOIN categories ON category_id = categories.id WHERE entries.user_id=?", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST method
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation doesn't match", 400)

        # Check if username already exists
        if db.execute("SELECT username FROM users WHERE username=?", request.form.get("username")):
            return apology("username already exists", 400)

        # Add username and password hash to db
        user = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", user, hash)

        # log user in
        id = db.execute("SELECT id FROM users WHERE username=?", user)
        session["user_id"] = id[0]["id"]

        # redirects user to home page
        return redirect("/")

    # User reached route via GET method
    else:
        return render_template("/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST method
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET method
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/personal", methods=["GET", "POST"])
@login_required
def personal():
    """personal page"""
    # List all the user's categories
    cat = db.execute("SELECT category FROM categories WHERE user_id=?", session["user_id"])
    categories = []
    for i in range(len(cat)):
        categories.append(cat[i]['category'])
    sorted_cat = sorted(categories)

    # User reached route via POST method
    if request.method == "POST":
        # Ensure user typed a category
        if not request.form.get("category"):
            return apology("please add a category", 400)

        # Ensure category doesn't already exist
        if request.form.get("category") in categories:
            return apology("category already exists", 400)

        db.execute("INSERT INTO categories (category,user_id) VALUES (?,?)", request.form.get("category"), session["user_id"])
        return redirect("/personal")

    # User reached route via Get method
    else:
        return render_template("personal.html", sorted_cat=sorted_cat)


@app.route("/security", methods=["GET", "POST"])
@login_required
def security():
    """Security page"""
    # User reached route via POST method
    if request.method == "POST":

        # Ensure current password is correct
        hash = db.execute("SELECT hash FROM users WHERE id=?", session["user_id"])
        if not check_password_hash(hash[0]["hash"], request.form.get("currentpassword")):
            return apology("incorrect password", 400)

        # Ensure password was submitted
        elif not request.form.get("newpassword"):
            return apology("must provide a new password", 400)

        # Ensure password and confirmation match
        elif request.form.get("confirmpassword") != request.form.get("newpassword"):
            return apology("new passwords doesn't match", 400)

        hash = generate_password_hash(request.form.get("newpassword"))
        db.execute("UPDATE users SET hash=? WHERE id=?", hash, session["user_id"])
        return redirect("/")

    # User reached route via Get method
    else:
        return render_template("security.html")


@app.route("/entry", methods=["GET", "POST"])
@login_required
def entry():
    """entry page"""
    # List all the user's categories
    cat = db.execute("SELECT category FROM categories WHERE user_id=?", session["user_id"])
    categories = []
    for i in range(len(cat)):
        categories.append(cat[i]['category'])
    sorted_cat = sorted(categories)

    # User reached route via POST method
    if request.method == "POST":
        # Ensure user input a +ve number in expense
        try:
            if float(request.form.get("expense")) <= 0:
                return apology("expense must be a positive value", 400)
        except:
            return apology("invalid input", 400)

        # Ensure category doesn't already exist
        if request.form.get("category") not in categories:
            return apology("category doesn't exists", 400)

        # Ensure user input date
        if not request.form.get("date"):
            return apology("must add a date", 400)

        # add entry to db
        cat_id = db.execute("SELECT id FROM categories WHERE category = ?", request.form.get("category"))
        db.execute("INSERT INTO entries (amount,description,date,user_id,category_id) VALUES (?,?,?,?,?)"
                , request.form.get("expense"), request.form.get("note"), request.form.get("date"), session["user_id"], cat_id[0]["id"])

        return redirect("/")

    # User reached route via Get method
    else:
        return render_template("entry.html", sorted_cat=sorted_cat)

