import numpy as np
import pandas as pd
from cs50 import SQL

import plotly
# import plotly.graph_objs as go

# date = np.datetime64('2002-07-30')

# print (date.astype(object).year)
# print (date.astype(object).month)
# print (date.astype(object).day)

# date = np.datetime64('today')

date_y = np.datetime64('today').astype(object).year
date_m = np.datetime64('today').astype(object).month
# date_d = np.datetime64('today').astype(object).day
# print(date_y, date_m, date_d)

db = SQL("sqlite:///expenses.db")
history = db.execute(""" SELECT amount, year, month, day, categories.category
            FROM entries INNER JOIN categories ON category_id = categories.id
            WHERE year=? AND month=? AND entries.user_id=?"""
            ,date_y, date_m, 1)

# create DataFrame from history
df = pd.DataFrame.from_dict(history)
df["date"] = df["year"].astype(str) + "-" + df["month"].astype(str) + "-" + df["day"].astype(str)
df["date"] = pd.to_datetime(df["date"])
df = df.drop(columns=['year', 'month', 'day'])

# Insert zero values for unused days
start = str(date_y) + "-" + str(date_m) + "-" + str(1)
end = pd.Series(pd.date_range(start, freq="M", periods=1))
period = np.datetime64(end[0]).astype(object).day

# Zero values dataframe for all days of the month
list = pd.DataFrame({'amount':None, 
                   'category':"-",
                   'date':pd.date_range(start, freq="D", periods=period)})

# Concat both df and list
df = pd.concat([df,list]).sort_values(['date', 'amount'], ascending=[True, False])

total = df["amount"].sum()
print(total)


import plotly.express as px

fig1 = px.bar(df, x="date", y="amount", color="category", text_auto=True)
# Plot to html
fig1.update_layout(showlegend=False, 
            xaxis = dict(tick0=0, dtick = 2*86400000, ticklabelmode="instant", tickangle= -45
            ))

config = {'displayModeBar': False}
# plotly.offline.plot(fig1,filename='tmp_fig1.html',config=config)

print(df)

fig2 = px.pie(df, values='amount', names='category')
plotly.offline.plot(fig2,filename='tmp_fig2.html',config=config)
