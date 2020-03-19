"""First linear regression
Removing values with the highest residuals
Second regression """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
#from sklearn.linear_model import LinearRegression
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd

style.use('ggplot')

#file to be plotted needs to be in the same folder
file = "ALGO"

#using pandas Dataframe
Df = pd.read_csv(file , delim_whitespace=True, comment = '%',header=None)
Df.columns = ["date", "x", "y", "z"]


#plotting dates
dates = Df["date"]
x = [dt.datetime.strptime(d,'%y%b%d').date() for d in dates]
print(x)
y = Df["x"]

ax = plt.gca()
formatter = mdates.DateFormatter("%y-%m-%d")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
plt.plot(x,y)



plt.show()
