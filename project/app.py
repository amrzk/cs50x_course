import os
import plotly
import plotly.express as px
import numpy as np
import pandas as pd

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

# Place holder text (Gimmick)
place_holder = "Kittens"

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
    date_y = np.datetime64('today').astype(object).year
    date_m = np.datetime64('today').astype(object).month

    history = db.execute(""" SELECT amount, year, month, day, categories.category
                FROM entries LEFT JOIN categories ON category_id = categories.id
                WHERE year=? AND month=? AND entries.user_id=?""",date_y, date_m, session["user_id"])
    if len(history) == 0:
        return render_template("index.html", total=0)

    # create DataFrame from history
    df = pd.DataFrame.from_dict(history)
    df["date"] = df["year"].astype(str) + "-" + df["month"].astype(str) + "-" + df["day"].astype(str)
    df["date"] = pd.to_datetime(df["date"])
    df = df.drop(columns=['year', 'month', 'day'])

    # Replace NaN (removed categories) for Pickles
    df.category.fillna(value=place_holder, inplace=True)

    # total (amount)
    total = df["amount"].sum()

    # NULL values dataframe for all days of the month
    start = str(date_y) + "-" + str(date_m) + "-" + str("01")
    end = pd.Series(pd.date_range(start, freq="M", periods=1))
    period = np.datetime64(end[0]).astype(object).day

    list = pd.DataFrame({
        'amount':None, 'category':None,
        'date':pd.date_range(start, freq="D", periods=period)})

    # Concatenate both df and list
    df = pd.concat([df,list]).sort_values(['date', 'amount'], ascending=[True, False])

    # Create fig1
    fig1 = px.pie(df, values='amount', names='category', color_discrete_sequence=px.colors.qualitative.Safe,
         labels = dict(date="Date", amount="Money Spent", category="Categories"))
    fig1.update_layout(showlegend=True)
    fig1.update_traces(textposition='inside', textinfo='percent+label')

    # Create the fig2
    xaxis_start = pd.to_datetime(start) - pd.Timedelta(days=1)
    fig2 = px.bar(df, x="date", y="amount", color="category", text_auto=False,
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels = dict(date="Date", amount="Money Spent", category="Categories"))
    fig2.update_layout(
        showlegend=False, xaxis_title=None,
        xaxis = dict(dtick=2*86400000.0, tickmode='linear', ticklabelmode="instant",
        tickformat='%b-%d', tickangle= -45, autorange= False, range=[xaxis_start, end[0]]))
    fig2.update_traces(textangle=0, textposition="outside", cliponaxis=False)
    
    # Plot to html
    config = {'displayModeBar': False, 'staticPlot': False}
    plotly.offline.plot(fig1,filename='templates/fig1.html',config=config)
    plotly.offline.plot(fig2,filename='templates/fig2.html',config=config)

    return render_template("index.html", total=total)


@app.route("/fig1")
@login_required
def fig1():
    """Load fig1"""
    return render_template("fig1.html")


@app.route("/fig2")
@login_required
def fig2():
    """Load fig2"""
    return render_template("fig2.html")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    # User reached route via POST method
    if request.method == "POST":
        # check for remove_button
        if 'remove_button' in request.form:
            id = request.form['remove_button']
            db.execute("DELETE FROM entries WHERE user_id=? AND id=?", session["user_id"], id)
            return redirect("/history")
        return apology("entry doesn't exist", 400)

    # User reached route via GET
    else:
        # Look up the user's entries
        history = db.execute(""" SELECT amount, description, year, month, day, entries.id, categories.category
                    FROM entries LEFT JOIN categories ON category_id = categories.id
                    WHERE entries.user_id=?""", session["user_id"])

        try:
            history = pd.DataFrame.from_dict(history).sort_values(['day', 'month', 'year', 'amount'], ascending=False)
        except:
            history = pd.DataFrame.from_dict(history)
            history['category'] = None
            
        # Replace NaN(removed categories) for Pickles
        history.category.fillna(value=place_holder, inplace=True)
        history = history.to_dict('records')
            

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
    cat = db.execute("SELECT id, category FROM categories WHERE user_id=?", session["user_id"])
    try:
        cat = pd.DataFrame.from_dict(cat).sort_values(['category']).reset_index()
    except:
        cat = pd.DataFrame.from_dict(cat)
        cat['category'] = None

    # User reached route via POST method
    if request.method == "POST":

        # check for remove_button
        if 'remove_button' in request.form:
            id = request.form['remove_button']
            
            # id not in database
            db_id = db.execute("SELECT * FROM categories WHERE user_id=? AND id=?", session["user_id"], id)
            if len(db_id) == 0:
                return apology("category doesn't exist", 400)
            
            db.execute("DELETE FROM categories WHERE user_id=? AND id=?", session["user_id"], id)
            return redirect("/personal")

        # check for add_button
        elif 'add_button' in request.form:
            # Ensure user typed a category
            if not request.form.get("category"):
                return apology("please add a category", 400)
            print(request.form.get('category'))
            # Ensure category doesn't already exist
            if request.form.get("category") in cat['category'].unique():
                return apology("category already exists", 400)

            db.execute("INSERT INTO categories (category,user_id) VALUES (?,?)"
                        , request.form.get("category"), session["user_id"])
            return redirect("/personal")

        else:
            # POST method using an illegal button
            return apology("illegal entry", 400)
        
    # User reached route via Get method
    else:
        cat = cat.to_dict('records')
        return render_template("personal.html", cat=cat)


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

        # Ensure user input a valid date
        if not request.form.get("date"):
            return apology("must add a date", 400)
        try:
            date = np.datetime64(request.form.get("date"))
        except:
            return apology("invalid date", 400)

        # add entry to db
        cat_id = db.execute("SELECT id FROM categories WHERE category = ?", request.form.get("category"))
        db.execute("""INSERT INTO entries (amount,description,year,month,day,user_id,category_id) 
                    VALUES (?,?,?,?,?,?,?)"""
                    , request.form.get("expense"), request.form.get("note")
                    , date.astype(object).year, date.astype(object).month, date.astype(object).day
                    , session["user_id"], cat_id[0]["id"])

        return redirect("/")

    # User reached route via Get method
    else:
        return render_template("entry.html", sorted_cat=sorted_cat, place_holder=place_holder)

