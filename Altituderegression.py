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

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.ticker import FormatStrFormatter
# Importing conversion function
from ConversionXYZ2NEU import  rotation

#linear plotter
def abline(slope, intercept, indexdates, datetimedates,color,ax):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    y_vals = intercept + slope * indexdates
    ax.plot(datetimedates, y_vals, '--',color =color)



#file to be plotted (needs to be in the same folder)
#pandas Dataframe
#Df = pd.read_csv(file , delim_whitespace=True, comment = '%',header=None)
#Df.columns = ["date", "x", "y", "z"]

file = r"PHKT.txt"
directory = r'C:\Users\JdeBo\Desktop\Q4 2019-2020\2020-Q3-project\NEU'
fullpath = os.path.join(directory,file)
with open(fullpath,'rb')  as pickle_file:
    data = pickle.load(pickle_file)
pickle_file.close()
ncolumns = int(len(data)/7)

data = np.reshape(data,(ncolumns,7))
Df = pd.DataFrame({'date': data[:, 0], 'N': data[:, 1], 'E':data[:,2], 'U':data[:,3],'sdN': data[:,4],'sdE':data[:,5], 'sdU':data[:,6]})
dates = Df['date']
dateslist = [dt.datetime.strptime(d,'%y%b%d').date() for d in dates]
daycount =[]
for day in dateslist:
    daycount.append((day-dateslist[0]).days)

Df["indexdates"] = daycount
Df.index = pd.to_datetime(Df['date'],format = '%y%b%d')
Df.drop(columns = ['date'], inplace = True)



Df['N'] = Df['N'].astype(float)
Df['E'] = Df['E'].astype(float)
Df['U'] = Df['U'].astype(float)
Df['sdN'] = Df['U'].astype(float)
Df['sdE'] = Df['U'].astype(float)
Df['sdU'] = Df['U'].astype(float)

N = Df['N'] #y axis to be plotted
E = Df['E']


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


# Linear regression assuming discontinuity
datespre   = indexeddates[0:split+1]
datespost  = indexeddates[split+1:]
print(datespre,datespost)

Npre       = N[0:split+1]
Npost      = N[split+1:]
Epre       = E[0:split+1]
Epost      = E[split+1:]


Nmodelpre   = LinearRegression().fit(datespre,Npre)
Emodelpre   = LinearRegression().fit(datespre,Epre)


Nb0pre      = Nmodelpre.intercept_
Nslopepre   = Nmodelpre.coef_
Eb0pre      = Emodelpre.intercept_
Eslopepre   = Emodelpre.coef_

NRsqpre     = Nmodelpre.score(datespre,Npre)
ERsqpre     = Emodelpre.score(datespre,Epre)


#polynomial interpolation
Npost = np.array(Npost)
Epost = np.array(Epost)
p1 = np.polyfit(daycount[split+1:], Npost, 10)
p2 = np.polyfit(daycount[split+1:], Epost, 10)

#interger to datetime coverting
xpre =[]
xpost =[]
for day in datespre:
    date = dateslist[0]+dt.timedelta(days=day[0].item())
    xpre.append(date)
for day in datespost:
    date = dateslist[0]+dt.timedelta(days=day[0].item())
    xpost.append(date)


#plotting
fig, axes = plt.subplots(nrows=3, ncols=1,sharex = True)



Df['N'].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9),color = 'red',grid = True, ax = axes[0])
Df['E'].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9),color = 'black',grid = True,ax = axes[1])
Df['U'].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9),color = 'blue',grid = True,ax = axes[2])

axes[0].set_ylabel('North mm')
axes[1].set_ylabel('East mm')
axes[2].set_ylabel('Up mm')

abline(Nslopepre,Nb0pre,datespre,xpre,"pink",axes[0])
abline(Eslopepre,Eb0pre,datespre,xpre,"pink",axes[1])


axes[0].plot(xpost, np.polyval(p1, daycount[split+1:]), 'b--', label='regression')
axes[1].plot(xpost, np.polyval(p2, daycount[split+1:]), 'b--', label='regression')
plt.show()