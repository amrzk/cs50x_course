import numpy as np


date = np.datetime64('2002-07-30')

print (date.astype(object).year)
print (date.astype(object).month)
print (date.astype(object).day)