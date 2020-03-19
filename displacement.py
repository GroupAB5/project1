from matplotlib import pyplot as plt
import numpy as np
import os

dir = 'C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/data/converted_data/'
files = []
for file in os.listdir(dir):
    files.append(file)

a = np.loadtxt(str(dir+files[0]), comments='%', usecols=(1, 2, 3))

#returns a list with dates
def get_dates(file_loc):
    file = open(file_loc, 'r')

    dates = []
    line = file.readlines()
    for i in range(2, len(line)):
        dates.append(line[i].split()[0])

    file.close()

    return dates

#print(get_dates(str(dir+files[0])))

def N_days(d1, d2):
    lib1 = {'JAN':31, 'FEB':28, 'MAR':31, 'APR':30, 'MAY':31}
    lib2 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY']

    day1 = int(d1[5:7])
    month1 = d1[2:5]
    year1 = int(d1[0:2])

    day2 = int(d2[5:7])
    month2 = d2[2:5]
    #year2 = int(d2[0:2])

    N = 0
    if month1 == month2:
        N = day2 - day1
    else:
        for i in range(lib2.index(month1), lib2.index(month2)+1):
            if i == lib2.index(month1):
                N += lib1[month1] - day1
            elif i == lib2.index(month2):
                N += day2
            else:
                if lib2[i] == 'FEB' and year1%4 == 0:
                    N += lib1[lib2[i]]+1
                else:
                    N += lib1[lib2[i]]

    return N

def displacement_rate(dates, coordinates):

    disp_x = []
    disp_y = []
    disp_z = []

    for i in range(len(coordinates)-1):
        x1, y1, z1 = coordinates[i]
        x2, y2, z2 = coordinates[i+1]

        disp_x.append(x2-x1)
        disp_y.append(y2-y1)
        disp_z.append(z2-z1)

    rate_x = []
    rate_y = []
    rate_z = []

    for j in range(len(disp_x)):
        rate_x.append((disp_x[j+1] - disp_x[j])/N_days(dates[j], dates[j+1]))     #calculates displacement per day
        rate_y.append((disp_y[j+1] - disp_y[j])/N_days(dates[j], dates[j+1]))
        rate_z.append((disp_z[j+1] - disp_z[j])/N_days(dates[j], dates[j+1]))

    return rate_x, rate_y, rate_z


#print(len(displacement_rate(0, a)))
#print(N_days('00JAN11', '00MAR01'))