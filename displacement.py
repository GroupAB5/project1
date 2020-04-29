from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
from matplotlib import style
from datetime import *
from ConversionXYZ2NEU import rotation
import rewriteFiles as rf
from mpl_toolkits.basemap import Basemap
from ConversionXYZ2NEU import latlongheight

# returns a list with dates
def get_dates(file_loc):
    file = open(file_loc, 'r')

    dates = []
    line = file.readlines()
    for i in range(2, len(line)):
        dates.append(line[i].split()[0])

    file.close()

    return dates


def N_days(d1, d2):
    #d1: initial date
    #d2: final date
    dt1 = datetime.strptime(d1, '%y%b%d').date()
    dt2 = datetime.strptime(d2, '%y%b%d').date()
    delta = dt2 - dt1

    return delta.days

#This method calculates the displacement rate in NEU coordinate system in meters per day
def displacement_rate_NEU(dates, coordinates):
    Dlist = []  #East
    Elist = []  #North
    Flist = []  #Up

    x, y, z = coordinates[len(coordinates)//2]

    for i in range(len(coordinates)- 1):
        D = 0
        E = 0
        F = 0

        x1, y1, z1 = coordinates[i]
        x2, y2, z2 = coordinates[i + 1]

        D, E, F = rotation(x, y, z, x2, y2, z2, x1, y1, z1)
        Dlist.append(D/N_days(dates[i], dates[i+1]))
        Elist.append(E/N_days(dates[i], dates[i+1]))
        Flist.append(F/N_days(dates[i], dates[i+1]))

    return Dlist, Elist, Flist

#I am not sure whether we need the function below
'''
def displacement_rate(dates, coordinates):
    disp_x = []
    disp_y = []
    disp_z = []

    for i in range(len(coordinates) - 1):
        x1, y1, z1 = coordinates[i]
        x2, y2, z2 = coordinates[i + 1]

        disp_x.append(x2 - x1)
        disp_y.append(y2 - y1)
        disp_z.append(z2 - z1)

    rate_x = []
    rate_y = []
    rate_z = []

    for j in range(len(disp_x)):
        rate_x.append(disp_x[j] / N_days(dates[j], dates[j + 1]))  # calculates displacement per day
        rate_y.append(disp_y[j] / N_days(dates[j], dates[j + 1]))
        rate_z.append(disp_z[j] / N_days(dates[j], dates[j + 1]))

    return rate_x, rate_y, rate_z
'''


#Not finished yet
def writeFile(location, name, date, position):
    file = open(location+name, 'w')
    file.write('%' + name + '\n')
    file.close()


def plot():
    dir = 'C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/data/converted_data/'

    files = []
    for file in os.listdir(dir):
        files.append(file)

    a = np.loadtxt(str(dir + files[0]), comments='%', usecols=(1, 2, 3))

    date = get_dates(dir+files[0])

    #xr, yr, zr = displacement_rate(date, a)
    xr, yr, zr = displacement_rate_NEU(date, a)

    style.use('ggplot')
    date = date[0:len(date) - 1]
    x = [datetime.strptime(d, '%y%b%d').date() for d in date]

    ax = plt.gca()
    formatter = mdates.DateFormatter("%y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)
    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    plt.plot(x, xr, label='East')
    plt.plot(x, yr, label='North')
    plt.plot(x, zr, label='Up')
    plt.legend()
    plt.ylabel('displacement[meters/day]')
    plt.show()

#plot()

def visualize():
    # Set basemap
    m = Basemap(width=12000000, height=9000000, projection='moll',
                resolution='c', lat_1=45., lat_2=55, lat_0=50, lon_0=-107.)
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='#cc9955', lake_color='aqua', zorder=0)
    m.drawcoastlines(color='0.15')


    dir = 'C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/data/converted_data/' #Change it to your directory

    files = []
    for file in os.listdir(dir):
        files.append(file)

    for i in range(len(files)):
        coordinates = np.loadtxt(str(dir + files[i]), comments='%', usecols=(1, 2, 3))

        stat_x = coordinates[:, 0]
        stat_y = coordinates[:, 1]
        stat_z = coordinates[:, 2]


        coord_transformed = [(latlongheight(stat_x[i], stat_y[i], stat_z[i])) for i in range(len(stat_x))]
        map_data = np.array(coord_transformed)

        lat = map_data[:, 1]  # latitude
        lon = map_data[:, 2]  # longitude

        # convert to map coordinates
        xpt, ypt = m(lon, lat)
        plt.plot(xpt, ypt, 'b')

        u = xpt[-1] - xpt[0]
        v = ypt[-1] - ypt[0]
        m.quiver(xpt[0], ypt[0], u, v, color='r')

    plt.show()

visualize()