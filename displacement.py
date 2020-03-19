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