from cs50 import SQL

db = SQL("sqlite:///expenses.db")

cat = db.execute("SELECT category FROM categories WHERE user_id=?", 1)
categories = []
for i in range(len(cat)):
    categories.append(cat[i]['category'])
sorted_cat = sorted(categories)
print(sorted_cat)