import numpy as np
import os

dir = 'C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/data/converted_data/'
files = []
for file in os.listdir(dir):
    files.append(file)

a = np.loadtxt(str(dir+files[0]), comments='%', usecols=(1, 2, 3))
print(a)

