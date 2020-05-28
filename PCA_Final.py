#Important importing
import pandas as pd
import numpy as np
import random as rd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import os
from displacement import displacement_rate_NEU

#load the data

dir = 'C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/data/converted_data/'

files = []
for file in os.listdir(dir):
    files.append(file)

stations = []
disp = []
for f in files:
    coor = []
    dates = []

    stations.append(str(f))

    fi = open(str(dir + f), 'r')
    lines = fi.readlines()
    for i in range(2, len(lines)):
        dates.append(lines[i][0:7].replace('\t', ''))
    fi.close()

    coor = np.loadtxt(str(dir + f), comments='%', usecols=(1, 2, 3))
    e, n, u = displacement_rate_NEU(dates, coor)
    disp.append([n[0], e[0], u[0]])

'''
file = 'C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/data/converted_data/ALGO'
coordinates = np.loadtxt(file, comments='%', usecols=(1, 2, 3))
date = []
f = open(file, 'r')

lines = f.readlines()
for i in range(2, len(lines)):
     date.append(lines[i][0:7].replace('\t', ''))

rates_E, rates_N, rates_U = displacement_rate_NEU(date, coordinates)
f.close()
'''

#Test Dataset
#genes = ['gene' + str(i) for i in range(1,101)]
wt = ['wt' + str(i) for i in range(1,4)]
data = pd.DataFrame(columns=['north', 'east', 'up'], index=stations)
for i in range(len(data.index)):
    data.loc[stations[i], 'north':'up'] = disp[i]

#Prints Dataset and Size of Dataset
print(data.head())
print(data.shape)

#Center and Scale the Data
scaled_data = preprocessing.scale(data)

"""
Dataset table should have x,y and z in y axis and stations in x axis
"""

#Create PCA object and do PCA
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)


#Plot
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

#Plot for Influence of Variables (basically percentages of what variables influence the PCA the most)
plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal Component')
plt.title('Scree Plot')
plt.show()

#Actual PCA Plot
pca_df = pd.DataFrame(pca_data, index=stations, columns=labels)

plt.scatter(pca_df.PC1, pca_df.PC2)
plt.title('PCA Graph')
plt.xlabel('PC1 - {0}%'.format(per_var[0]))
plt.ylabel('PC2 - {0}%'.format(per_var[1]))

for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))
plt.show()