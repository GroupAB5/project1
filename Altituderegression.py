"""This Script plots data points in from  files converted by adam
It will also plot three different linear regressions one red line over the complete data one line pink using
data points from before the 2004 earthquake and one green using data points post earthquake
To plot linear regression from a different file change the file name
Note the x-axis numbers show the days counted from the first date in the file"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.linear_model import LinearRegression
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd
import pickle
import os
from matplotlib.ticker import FormatStrFormatter
# Importing conversion function
from ConversionXYZ2NEU import  rotation

#linear plotter
def abline(slope, intercept, x_vals, color):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--',color =color)



#file to be plotted (needs to be in the same folder)
#pandas Dataframe
#Df = pd.read_csv(file , delim_whitespace=True, comment = '%',header=None)
#Df.columns = ["date", "x", "y", "z"]

file = r"ALGO.txt"
directory = r'C:\Users\JdeBo\Desktop\Q4 2019-2020\2020-Q3-project\NEU'
fullpath = os.path.join(directory,file)
with open(fullpath,'rb')  as pickle_file:
    data = pickle.load(pickle_file)
pickle_file.close()
ncolumns = int(len(data)/7)

data = np.reshape(data,(ncolumns,7))
Df = pd.DataFrame({'date': data[:, 0], 'N': data[:, 1], 'E':data[:,2], 'U':data[:,3],'sdN': data[:,4],'sdE':data[:,5], 'sdU':data[:,6]})
print(Df.head(), Df.tail())
dates = Df['date']
dateslist = [dt.datetime.strptime(d,'%y%b%d').date() for d in dates]
daycount =[]
for day in dateslist:
    daycount.append((day-dateslist[0]).days)

Df["indexdates"] = daycount

Df['N'] = Df['N'].astype(float)
Df['E'] = Df['E'].astype(float)
Df['U'] = Df['U'].astype(float)
Df['sdN'] = Df['U'].astype(float)
Df['sdE'] = Df['U'].astype(float)
Df['sdU'] = Df['U'].astype(float)

y = Df['N'] #y axis to be plotted
print(y)











#Choosing the date to split the data On due to assumed discontinuity at earthquake
Data_quake = dt.datetime(2004,12,26) in dateslist
if Data_quake:
    split = dateslist.index(dt.datetime(2004,12,26)) + 1                          #+1 as to include 26 in pre earthquake
    print ('date of earth quake is included')
else:
    i = 0
    lst =[]
    for day in dates:
        if day.startswith("04DEC27" ) or day.startswith("04DEC28"  ) or day.startswith("04DEC29") or day.startswith("04DEC30") or day.startswith("04DEC31"):
            lst.append([day,i])
        i+=1
    if  not lst:                                                                              #checking if list is empty
        i = 0
        lst = []
        for day in dates:
            if day.startswith("05") or day.startswith("06") or day.startswith("07") or day.startswith("08") \
                    or day.startswith("09") or day.startswith("10") or day.startswith("11") or day.startswith("12") \
                    or day.startswith("13") or day.startswith("14") :
                lst.append([day,i])
            i += 1
    split = lst[0][1]
    print("date of earthquake is not present data is split on :",lst[0][0])



#linear regression over all dates with dates as input z valuies as output
indexeddates = np.array(daycount).reshape(-1,1) #using indexes instead of actual dates.]
model        = LinearRegression().fit(indexeddates,y)
Rsq          = model.score(indexeddates,y)
b0           = model.intercept_
slope        = model.coef_

# Linear regression assuming discontinuity
datespre   = indexeddates[0:split]
datespost  = indexeddates[split:-1]

zpre       = y[0:split]
zpost      = y[split:-1]

modelpre   = LinearRegression().fit(datespre,zpre)
modelpost  = LinearRegression().fit(datespost,zpost)

b0pre      = modelpre.intercept_
b0post     = modelpost.intercept_

slopepre   = modelpre.coef_
slopepost  = modelpost.coef_

Rsqpre     = modelpre.score(datespre,zpre)
Rsqpost    = modelpost.score(datespost,zpost)

#polynomial interpolation
zpost = np.array(zpost)
p = np.polyfit(daycount[split+1:], zpost, 10)


#plotting

Df.plot(kind='scatter',x= 'indexdates',y= 'N',color ='red')
abline(slopepre,b0pre,datespre,"pink")
#abline(slopepost,b0post,datespost,"green")

plt.plot(daycount[split+1:], np.polyval(p, daycount[split+1:]), 'b--', label='regression')

plt.show()