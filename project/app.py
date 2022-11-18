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
    # # retrieving user's history
    # data = db.execute("SELECT symbol, shares FROM purchase WHERE user_id=?", session["user_id"])

    # # Combining entries for same company
    # purchase = []
    # symbols = []
    # for i in range(len(data)):
    #     if data[i]["symbol"] in symbols:
    #         purchase[symbols.index(data[i]["symbol"])]["shares"] += data[i]["shares"]
    #     else:
    #         quote = lookup(data[i]["symbol"])
    #         quote["shares"] = data[i]["shares"]
    #         purchase.append(quote)
    #         symbols.append(data[i]["symbol"])

    # # Calculating totals
    # stock = 0
    # for i in range(len(purchase)):
    #     stock += purchase[i]["shares"] * purchase[i]["price"]
    #     purchase[i]["total"] = usd(purchase[i]["shares"] * purchase[i]["price"])
    #     purchase[i]["price"] = usd(purchase[i]["price"])

    # cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    # total = usd(cash[0]["cash"] + stock)
    # cash = usd(cash[0]["cash"])

    # return render_template("index.html", purchase=purchase, cash=cash, total=total)
    return apology("Not Implemented", 404)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # request via POST verify symbol and render quoted.html
    if request.method == "POST":
        # # Check for symbol
        # if not lookup(request.form.get("symbol")):
        #     return apology("Invalid ticker symbol", 400)

        # # Check shares (+ve int)
        # try:
        #     if float(request.form.get("shares")) % 1 != 0 or int(request.form.get("shares")) < 1:
        #         return apology("Invalid number of shares", 400)
        # except:
        #     return apology("Invalid number of shares", 400)

        # # Check balance
        # quote = lookup(request.form.get("symbol"))
        # change = int(request.form.get("shares")) * quote["price"]
        # balance = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])

        # # Check if user have enough money
        # if balance[0]["cash"] < change:
        #     return apology("Your balance is not enough", 400)

        # date = datetime.now().replace(microsecond=0)
        # symbol = str(request.form.get("symbol")).upper()
        # shares = request.form.get("shares")
        # # update database with new balance & purchase data
        # db.execute("UPDATE users SET cash=? WHERE id=?", balance[0]["cash"] - change, session["user_id"])
        # db.execute("INSERT INTO purchase (symbol,price,shares,date,user_id) VALUES (?,?,?,?,?)",
        #            symbol, quote["price"], shares, date, session["user_id"])

        # return redirect("/")
        return apology("Not Implemented", 404)

    # request via GET render buy.html
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # history = db.execute("SELECT symbol, price, shares, date FROM purchase WHERE user_id=?", session["user_id"])
    # return render_template("history.html", history=history)
    return apology("Not Implemented", 404)


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


@app.route("/profile")
@login_required
def profile():
    """Profile page"""

    # User reached route via POST method
    if request.method == "POST":
        return apology("not implemented", 404)

    # User reached route via Get method
    else:
        user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        return render_template("profile.html", user=user)
# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     """Get stock quote."""
#     # request via POST verify symbol and render quoted.html
#     if request.method == "POST":
#         # Check for symbol
#         if not lookup(request.form.get("symbol")):
#             return apology("Invalid ticker symbol", 400)
#         # render / populate quoted.html
#         quote = lookup(request.form.get("symbol"))
#         return render_template("quoted.html", symbol=quote["symbol"], name=quote["name"], price=usd(quote["price"]))

#     # request via GET render quote.html
#     else:
#         return render_template("quote.html")


# @app.route("/sell", methods=["GET", "POST"])
# @login_required
# def sell():
#     """Sell shares of stock"""

#     # Company symbols of which the user own shares
#     symbol = db.execute("SELECT DISTINCT symbol FROM purchase WHERE user_id=?", session["user_id"])
#     symbols = []
#     for i in range(len(symbol)):
#         symbols.append(symbol[i]["symbol"])

#     if request.method == "POST":
#         # Check for symbol
#         if not lookup(request.form.get("symbol")):
#             return apology("Company not found", 404)

#         if not request.form.get("symbol") in symbols:
#             return apology("You don't own shares for this company", 404)

#         # Check shares (+ve int)
#         if float(request.form.get("shares")) % 1 != 0 or int(request.form.get("shares")) < 1:
#             return apology("Invalid input", 400)

#         # Check shares being sold with the user's total shares
#         shares = 0
#         data = db.execute("SELECT shares FROM purchase WHERE user_id=? AND symbol=?",
#                           session["user_id"], request.form.get("symbol"))
#         for i in range(len(data)):
#             shares += data[i]["shares"]
#         if int(request.form.get("shares")) > shares:
#             return apology(str(data), 400)

#         # Check balance
#         quote = lookup(request.form.get("symbol"))
#         change = int(request.form.get("shares")) * quote["price"] * (-1)
#         balance = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
#         date = datetime.now().replace(microsecond=0)
#         symbol = request.form.get("symbol")
#         shares = int(request.form.get("shares")) * (-1)
#         # update database with new balance & purchase data
#         db.execute("UPDATE users SET cash=? WHERE id=?", balance[0]["cash"] - change, session["user_id"])
#         db.execute("INSERT INTO purchase (symbol,price,shares,date,user_id) VALUES (?,?,?,?,?)",
#                    symbol, quote["price"], shares, date, session["user_id"])

#         return redirect("/")

#     # request via GET render sell.html
#     else:
#         return render_template("sell.html", symbols=symbols)