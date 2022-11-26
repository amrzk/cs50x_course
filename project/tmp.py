import numpy as np
import pandas as pd
from cs50 import SQL

import plotly
import plotly.graph_objs as go

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
df = df.sort_values(by="date")
df = df.reset_index(drop=True)


# Insert zero values for unused days
start = str(date_y) + "-" + str(date_m) + "-" + str(1)
end = pd.Series(pd.date_range(start, freq="M", periods=1))
print(start)
print(end[0])
period = np.datetime64(end[0]).astype(object).day
print(period)
srs = pd.Series(pd.date_range(start, freq="D", periods=period))
print(srs)



# Lump all entries in 1 day 
df1 = df.copy()
df1['Total'] = df.groupby(['date'])['amount'].transform('sum')
df1 = df1.drop_duplicates(subset=['date'])

# Lump all category entries in 1 day 
# df2= df.copy()
# df2['Total'] = df.groupby(['date', 'category'])['amount'].transform('sum')
# df2 = df2.drop_duplicates(subset=['date', 'category'])

# Create a trace
data = [go.Scatter(
x = df1['date'],
y = df1['amount'],
)]
layout = go.Layout(
xaxis=dict(title='date'),
yaxis=dict(title='amount')
)

# Plot to html
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig,filename='fig1.html',config={'displayModeBar': False})