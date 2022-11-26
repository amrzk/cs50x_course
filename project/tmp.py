import numpy as np
import pandas as pd
from cs50 import SQL

import matplotlib.pyplot as plt

# date = np.datetime64('2002-07-30')

# print (date.astype(object).year)
# print (date.astype(object).month)
# print (date.astype(object).day)

# date = np.datetime64('today')

date_y = np.datetime64('today').astype(object).year
date_m = np.datetime64('today').astype(object).month
# date_d = date.astype(object).day
# print(date_y, date_m, date_d)

db = SQL("sqlite:///expenses.db")
history = db.execute(""" SELECT amount, year, month, day, categories.category
            FROM entries INNER JOIN categories ON category_id = categories.id
            WHERE year=? AND month=? AND entries.user_id=?"""
            ,date_y, date_m, 1)


df = pd.DataFrame.from_dict(history)
df["date"] = df["year"].astype(str) + "-" + df["month"].astype(str) + "-" + df["day"].astype(str)
df["date"] = pd.to_datetime(df["date"])
df = df.drop(columns=['year', 'month', 'day'])
df.sort_values(by="date")

df.plot()
plt.show()