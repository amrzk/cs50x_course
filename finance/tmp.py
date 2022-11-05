import os

from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


data = db.execute("SELECT symbol, shares FROM purchase WHERE user_id=?", 8)
purchase = []
symbols = []
for i in range(len(data)):
    if data[i]["symbol"] in symbols:
        purchase[symbols.index(data[i]["symbol"])]["shares"] += data[i]["shares"]
    else:
        purchase.append(data[i])
        symbols.append(data[i]["symbol"])




print(purchase)