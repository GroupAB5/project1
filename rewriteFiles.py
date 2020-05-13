'''
This file rewrites the gps data files
'''

import numpy as np
import os
from displacement import get_dates, N_days
from datetime import *

#this method reads coordinate data from gipsy files
def getCoord(f):
    file = open(f, 'r')

    lines = file.readlines()

    date = lines[0][20:27]

    k = 0
    for line in range(1, len(lines)):
        if lines[line][7:8] == ' ':
            k = line
            break

    coordinates = []
    stations = []

    for i in range(1, k, 3):
        stations.append(lines[i].split()[1])

        xyz = []
        for j in range(3):
            xyz.append(float(lines[i+j].split()[4]))

        coordinates.append(xyz)

    file.close()

    coordinates = np.array(coordinates)

    return coordinates, stations, date

#This is no longer needed for the project because all the files are already rewritten
files = []
dir = 'gps_data'
for file in os.listdir(dir):
    files.append(file)


def rewrite():
    coordinates, stations, date = getCoord('gps_data/'+files[0])

    for i in range(len(stations)):
        file = open('converted_data/'+stations[i], 'w')
        file.write('%'+stations[i]+' Station \n')
        file.write('%date'+'\t\t\t'+'x'+'\t\t\t\t\t'+'y'+'\t\t\t\t\t'+'z \n')

        file.write(date+'\t'+str(coordinates[i][0])+'\t'+str(coordinates[i][1])+'\t'+str(coordinates[i][2])+'\n')

        file.close()

#rewrite()

def addToFiles():

    for i in range(1, len(files)):
        coordinates, stations, date = getCoord('gps_data/'+files[i])

        for j in range(len(stations)):
            file_content = []
            dir = 'converted_data'
            for file in os.listdir(dir):
                file_content.append(file)

            if stations[j] in file_content:
                f = open('converted_data/'+stations[j], 'a')
                f.write(date + '\t' + str(coordinates[j][0]) + '\t' + str(coordinates[j][1]) + '\t' + str(
                    coordinates[j][2]) + '\n')
                f.close()
            else:
                f = open('converted_data/'+stations[j], 'w')
                f.write('%' + stations[j] + ' Station \n')
                f.write('%date' + '\t\t\t' + 'x' + '\t\t\t\t\t' + 'y' + '\t\t\t\t\t' + 'z \n')
                f.write(date + '\t' + str(coordinates[j][0]) + '\t' + str(coordinates[j][1]) + '\t' + str(
                    coordinates[j][2]) + '\n')
                f.close()
#addToFiles()

def rewrite2():
    file_content = []
    dir = 'converted_data'
    for file in os.listdir(dir):
        file_content.append(file)

    for file in file_content:
        f = open(str('converted_data/'+file), 'r')
        l = f.readlines()
        f.close()

        a = np.loadtxt(str('converted_data/'+file), comments='%', usecols=(1, 2, 3))
        x, y, z = a[:, 0], a[:, 1], a[:,2]

        dates = get_dates(str('converted_data/'+file))
        dates.sort(key=lambda date: datetime.strptime(date, '%y%b%d'))

        f = open('C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/data/converted_data/'+file, 'w')
        f.write(l[0])
        f.write(l[1])
        for d in dates:
            for i in range(2, len(l)):
                if d == l[i].split()[0]:
                    f.write(l[i])
                    continue

        f.close()

#rewrite2()