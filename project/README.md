# <img src="/static/favicon.ico" alt="drawing" width="7.5%"/> C$50 Expense - CS50X Final Project 2022
C$50 Expense is a web-based application that enables the user to log their daily expenses and neatly plot some graphs for the user to monitor their spending.

[See it in action.](https://www.google.com)

### The Main Features of C$50 Expense:

## Personalized:
This feature allows the user to create their own unique categories to represent their purchase. It also gives the user the ability to remove unwanted categories.

## Adding A New Transaction:
This feature allows the user to add a new transaction. Any transaction must contain the amout of money spent, the category the transaction belongs to, the date of the transaction (year-month-day). User can also add a note for their transactions, this is to further help the user distinguish between their entries (which is an optional field).

## The Front Page:
The front page presents the user with easy to understand graphs representing the user's transactions and their relative categories in the span of the current month [This feature is planned to have future development].

## Other features:
The web app allows the user to create their own personal account, changing their password as they want.

The user may also view their history page which allows them to remove any unwanted or wrong transaction.

# Example Workflow:
After the user create their own account .....

# Structure And Files:
C$50 Expense is a python written app, supported by sqlite3 database, and using flask to host and run the app and jinja for templating. Bootstrap library is used to layout/style. Plotly and plotly express to plot the graphs for the user. 

### Main Files:
- app.py file contains majority of the code and is responsible for relaying the data sent by the user to the database or back to the user after a series of guard clauses.

- helpers.py file contains a couple of helper functions that are called in the app.py file which helps keeping the main (app,py) file clean and neat.

# Struggles And Design Choices:
### Choices:
- SQL database; three tables where used to represent:
    + The users table containing a unique id, username, and the hashed password for each user.
    + the categories table containing a unique id, name of the category, the user_id of the user who created the category.
    + the entries table containing a unique id, money spent, date (depicted in the form of day, month, and year in separate columns), user_id, and category_id. 

- Pandas library for python was picked to easly manipulate the user's data outputted form SQL and eventually using these dataframes anlong side the plotly library to get the desired graphs.  

- Plotly Offline Plot was used to create the < div > part of the graphs which ar then relaid to the html through jinja code.

### Struggles:
- Allowing the user to remove a category was a difficult choice to make because there is always the problem of the entries using that category, henceforth the following was decided:
    + The category_id column in entries table will not be a (FOREIGN KEY) to allow the user to remove a category without having to remove all related entries to that category.
    + All (NaN) category names will be represented by a generic category name to represent all the entries that had their category removed.

# Future Development:
The ability to allow the user to freely pick the time period for the graphs instead of statically showing the data of the current month only.
