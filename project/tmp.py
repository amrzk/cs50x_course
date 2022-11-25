from cs50 import SQL


db = SQL("sqlite:///expenses.db")
db.execute("INSERT INTO entries (amount,description,date,user_id,category_id) VALUES (?,?,?,?,?)"
        ,  12.5, 'tomatos', '11/17/2022', 1, 7)