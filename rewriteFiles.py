'''
This file rewrites the gps data files
'''

import numpy as np

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
'''
files = []
xval = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '99']
for x in xval:
    for i in range(1, 126):
        if i < 10:
            k = 'PZITRF0800' + str(i) + '.' + x + 'X'
        elif i < 100:
            k = 'PZITRF080' + str(i) + '.' + x + 'X'
        else:
            k = 'PZITRF08' + str(i) + '.' + x + 'X'
        files.append(k)


def rewrite():
    coordinates, stations, date = getCoord('gps_data/'+files[0])

    for i in range(len(stations)):
        file = open('converted_data/'+stations[i], 'w')
        file.write('%'+stations[i]+' Station \n')
        file.write('%date'+'\t\t\t'+'x'+'\t\t\t\t\t'+'y'+'\t\t\t\t\t'+'z \n')

        file.write(date+'\t'+str(coordinates[i][0])+'\t'+str(coordinates[i][1])+'\t'+str(coordinates[i][2])+'\n')

        file.close()

#rewrite()

import os
file_content = []
dir = 'C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/program/converted_data'
for file in os.listdir(dir):
    file_content.append(file)

def addToFiles():

    for i in range(1, len(files)):
        coordinates, stations, date = getCoord('gps_data/'+files[i])

        for j in range(len(stations)):
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
addToFiles()
'''