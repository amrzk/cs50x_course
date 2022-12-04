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
# df = df.to_dict('records')
x = pd.to_datetime("today")
today = pd.to_datetime("today")
date_y = pd.to_datetime("today").year
date_m = pd.to_datetime("today").month
date_d = pd.to_datetime("today").day

start = str(date_y) + "-" + str(date_m) + "-" + str("01")
end = pd.Series(pd.date_range(start, freq="M", periods=1))

period = (end[0] - pd.to_datetime(start) + pd.Timedelta(days=1)).days

print(pd.to_datetime(x, format='%Y%b%d'))


plot_ly(data_for_plot, labels = ~cyl, values = ~n, type = 'pie', hole = 0.05 ,textposition = 'outside',textinfo = 'percent') %>%
  layout(title = list(text = "my nice title is here", xanchor = "center"),
         showlegend = F,
         margin = list(l = 20, r = 20),
         xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = TRUE),
         yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = TRUE)) %>%
  layout(paper_bgcolor = "pink")
  
  
  
# %%
# import plotly
# import plotly.graph_objects as go
# fig = go.Figure()
# fig.add_scatter(x=[1, 3], y=[5, 4])
# fig.add_scatter(x=[1, 10], y=[5, 4])
# fig.update_layout("autorange": false, "range": ["2020-01-01", "2020-12-31"],)

# config = {'displayModeBar': False, 'staticPlot': False}
# plotly.offline.plot(fig,filename='fig.html',config=config)
# %%
