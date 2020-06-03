"""This Script plots data points in from  files converted by adam
It will also plot three different linear regressions one red line over the complete data one line pink using
data points from before the 2004 earthquake and one green using data points post earthquake
To plot linear regression from a different file change the file name
Note the x-axis numbers show the days counted from the first date in the file"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
from sklearn.linear_model import LinearRegression
from scipy.optimize import newton,bisect
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
    ax.plot(datetimedates, y_vals, '--',color = color)

directory = r'C:\Users\JdeBo\Desktop\Q4 2019-2020\2020-Q3-project\NEU'

def timeseries(filename, mode="show"):
    """Generate plots from a pickle file, mode is either save to write to disk or default show to see a specific time series"""

    fullpath = os.path.join(directory, filename)
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
        split = dateslist.index(dt.datetime(2004,12,26))                          #+1 as to include 26 in pre earthquake
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
    datespre   = indexeddates[0:split]
    datespost  = indexeddates[split:]


    Npre       = N[0:split]
    Npost      = N[split:]
    Epre       = E[0:split]
    Epost      = E[split:]


    #polynomial regression
    Npost = np.array(Npost)
    Epost = np.array(Epost)
    p1 = np.polyfit(daycount[split:], Npost, 10)
    p2 = np.polyfit(daycount[split:], Epost, 10)

    #derivatives
    dNddate = np.polyder(p1)
    dEddate = np.polyder(p2)
    d2Nddate2 =np.polyder(dNddate)
    d2Eddate2 =np.polyder(dEddate)

    #solving when slope after earthquake becomes equal to before
    if len(Npre)>1 :

        Nmodelpre = LinearRegression().fit(datespre, Npre)
        Emodelpre = LinearRegression().fit(datespre, Epre)

        Nb0pre = Nmodelpre.intercept_
        Nslopepre = Nmodelpre.coef_
        Eb0pre = Emodelpre.intercept_
        Eslopepre = Emodelpre.coef_

        NRsqpre = Nmodelpre.score(datespre, Npre)
        ERsqpre = Emodelpre.score(datespre, Epre)


        def f(x):
            return np.polyval(dNddate,x)-Nslopepre
        def g(x):
            return np.polyval(dEddate, x) - Eslopepre
        def dfdx(x):
            return np.polyval(d2Nddate2,x)
        def dgdx(x):
            return np.polyval(d2Eddate2,x)


        # Northlinear = newton(f,x0 =2200,fprime =dfdx,maxiter = 1000)
        # Eastlinear = newton(dgdx,x0= 2229, fprime=dgdx, maxiter=1000)
        try:
            Northlinear = bisect(f,2100,10000, maxiter=10000)
            Eastlinear = bisect(g,2000,10000,maxiter=10000)
            print('''For {}, North has the same slope as before eartquake at day {}
                    East has the same slope as before eartquake at day {}
                    this comes down to the dates {} and {}'''.format(filename[0:4], Northlinear, Eastlinear,
                                                                     dateslist[0] + dt.timedelta(
                                                                         days=round(Northlinear)),
                                                                     dateslist[0] + dt.timedelta(
                                                                         days=round(Eastlinear))))
        except:
            print('For {}, bisection does not converge or f(a)*f(b) > 0 '.format(filename[0:4]))






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
    fig, axs = plt.subplots(nrows=3, ncols=1,sharex = True)

    Df['N'].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9),color = 'red',grid = True, ax = axs[0])
    Df['E'].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9),color = 'black',grid = True,ax = axs[1])
    Df['U'].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9),color = 'blue',grid = True,ax = axs[2])

    # getting month subticks
    months = mdates.MonthLocator()

    axs[0].set_ylabel('North [m]')
    axs[0].xaxis.set_minor_locator(months)
    axs[0].ticklabel_format(axis='y', style='sci', useMathText=True)
    tik0 = axs[0].get_yticks()
    axs[0].set_ylim(tik0[0],tik0[-1])
    axs[0].set_yticks(tik0)

    axs[1].set_ylabel('East [m]')
    axs[1].xaxis.set_minor_locator(months)
    axs[1].ticklabel_format(axis='y', style='sci', useMathText=True)
    tik1 = axs[1].get_yticks()
    axs[1].set_ylim(tik1[0],tik1[-1])
    axs[1].set_yticks(tik1)

    axs[2].set_ylabel('Up [m]')
    axs[2].xaxis.set_minor_locator(months)
    axs[2].ticklabel_format(axis='y', style='sci', scilimits=(-1,-2), useMathText=True)
    if len(Npre)>1 :
        abline(Nslopepre,Nb0pre,datespre,xpre,"blue",axs[0])
        abline(Eslopepre,Eb0pre,datespre,xpre,"darkviolet",axs[1])


    axs[0].plot(xpost, np.polyval(p1, daycount[split:]), color = 'blue', label='regression', linestyle = "--")
    axs[1].plot(xpost, np.polyval(p2, daycount[split:]), color = 'darkviolet', label='regression', linestyle = "--")







    if mode == "show":
       plt.show()
      #multivariate polynomial fit
       # def fitFunc(NE,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9):
       #    return (a0 +a1*NE[0]+a2*NE[1]+a3*NE[0]*NE[0] + a4*NE[1]*NE[1] + a5*NE[0]*NE[1] + a6*NE[0]*NE[0]*NE[0]
       #      +a7*NE[1]*NE[0]*NE[0]+a8*NE[1]*NE[1]*NE[0]+a9*NE[1]*NE[1]*NE[1])
       # NE = np.array([Npost,Epost])
       # print(np.shape(NE),NE.dtype)
       # print(np.shape(datespost),datespost.dtype)
       # fitpoly = curve_fit(fitFunc,NE, np.array(datespost).flatten())
       # NElin = np.array([np.linspace(-0.5,-0.1,1000),np.linspace(-0.3,-0.1,1000)])
       # print(fitpoly[0])
       # #ax2.plot(NElin[0],NElin[1],fitFunc(NElin,fitpoly[0][0],fitpoly[0][1],fitpoly[0][2],fitpoly[0][3],fitpoly[0][4],fitpoly[0][5],fitpoly[0][6],
       #                                    fitpoly[0][7],fitpoly[0][8],fitpoly[0][9]))
       ax2 = plt.axes(projection='3d')
       extrapolate =np.arange(daycount[-1],2250,1)
       extradays = np.concatenate((daycount[split:],extrapolate), axis=None)
       ax2.plot(extradays,np.polyval(p1,extradays),np.polyval(p2,extradays),color = 'darkviolet',label ='regeression',linestyle = '--' ,linewidth =0.5)
       ax2.scatter(indexeddates,Df['N'], Df['E'],  cmap='viridis', linewidth=0.1);
       ax2.set_ylabel('North [mm]')
       ax2.set_zlabel('East [mm]')
       ax2.set_xlabel('Days')
       plt.show()

    if mode == "save":
        stat = filename[0:4] + ".png"# first four characters of the filename string
        print(stat)
        loc  = r"C:\Users\JdeBo\Desktop\Q4 2019-2020\2020-Q3-project\timeseries"
        plt.savefig(os.path.join(loc, stat))
        plt.close(fig)

# # execute this to see a specific station
# file = r"PHKT.txt"
# timeseries(file)

# execute this when you want all timeseries
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


for f in files:
    timeseries(f, mode="save")                  #Mode to save or see plots

