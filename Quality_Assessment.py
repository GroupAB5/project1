import numpy as np
from os import listdir
from os.path import isfile, join

def quality_matrix(standarddeviation):

    Qy = np.zeros((3, 3)) # size is always 3x3
    for i in range(3):
        Qy[i][i] = standarddeviation[i] ** 2 # the diagonal of Qx is the same as Qy
    return Qy


def covariance_matrix(correlation, standarddeviation):
    Qx = quality_matrix(standarddeviation)
    # fill non diagonal elements
    for element in correlation:
        i, j, correlation = element
        i = int((i - 1)% 3) # avoid index out of bound error
        j = int((j - 1)% 3)
        Qx[i, j] = correlation * np.sqrt(Qx[i, i]) * np.sqrt(Qx[j, j]) # transforming correlation to covariance
        Qx[j, i] = Qx[i, j] # symmetric matrix
    return Qx

def get_covmatrix(filename):
    directory = r'C:\Users\Mees de Graaf\Documents\Tu delft\project test analysis\GPS_Data\data' # remember to paste your own directory here
    with open(join(directory, filename)) as f:
        lines = f.readlines()
        first = lines[0].split() # read first line
        N_par = int(first[0]) + 1 # find number of parameters in order to get to correlation part
        date  = first[-1] # getting the date of the datafile

        # storing all prepared data in lists
        data_lines = lines[1:N_par]
        corr_lines = lines[N_par::]
        tags = []
        correlations = []
        corr_data = []
        sigmas = []
        std_dev_data = []
        output = []
        # getting standard deviations
        for line in data_lines:
            sigma = float(line.split()[-1])
            sigmas.append(sigma)
            # getting station names as tags
            if int(line.split()[0])% 3 == 1:
                tags.append(line.split()[1] + date)

        for idx in range(len(sigmas)):
            if idx % 3 == 0:
                std_dev_data.append([sigmas[idx], sigmas[idx+1], sigmas[idx+2]])

        # getting all correlations
        for corr_line in corr_lines:
            corri = tuple(map(float, corr_line.split()))
            correlations.append(corri)

        # structuring all correlations for all stations
        for idx in range(len(correlations)):
            if idx % 3 == 0:
                corr_data.append([correlations[idx], correlations[idx+1], correlations[idx+2]])

        # output is a list with all covariance matrices tagged by station and date
        for idx, corr in enumerate(corr_data):
            output.append([tags[idx], covariance_matrix(corr, std_dev_data[idx])])
        return output

# path to directory with all datafiles
mypath = r'C:\Users\Mees de Graaf\Documents\Tu delft\project test analysis\GPS_Data\data'
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))] # getting all filenames in a list

# call function for all files in your data file folder
if __name__ == "__main__":
    for file in filenames:
        if len(file) == 15: # only files with the regular filename should pass
            print(get_covmatrix(file)[0]) # fair bit of runtime (5845 files)



## This commented out bit is the structure of the correlation and standard deviation to construct one covariance matrix
# std_dev = [0.110641654490017E-02, 0.202139649818358E-02, 0.197912368098458E-02] # standard deviations from test_script
# corr = [(1, 2, 0.1),
#         (2, 3, -0.3),
#         (3, 1, 0.8)] # correlation between XY, YZ, XZ (this variable structure should be implemented for this to work)
