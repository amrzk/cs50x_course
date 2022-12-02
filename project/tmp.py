# %%

import os

import pandas as pd

from cs50 import SQL


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///expenses.db")


history = db.execute(""" SELECT amount, description, year, month, day, entries.id, categories.category
            FROM entries LEFT JOIN categories ON category_id = categories.id
            WHERE entries.user_id=?""", 1)


df = pd.DataFrame.from_dict(history)
df.category.fillna(value='Pickles', inplace=True)
df = df.to_dict('records')

# %%
import plotly
import plotly.graph_objects as go
fig = go.Figure()
fig.add_scatter(x=[1, 3], y=[5, 4])
fig.add_scatter(x=[1, 10], y=[5, 4])
fig.update_layout("autorange": false, "range": ["2020-01-01", "2020-12-31"],)

config = {'displayModeBar': False, 'staticPlot': False}
plotly.offline.plot(fig,filename='fig.html',config=config)
# %%
